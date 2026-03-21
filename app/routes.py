"""
API Routes - all the endpoints for the application
- /api/scan       -> analyze text for fake news/scams
- /api/history    -> get previous scan results
- /api/stats      -> get dashboard statistics
- /api/whatsapp/webhook -> handle incoming whatsapp messages
"""

from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ScanResult
from app.schemas import ScanRequest, ScanResponse
from app.groq_service import analyze_text
from app.whatsapp_service import format_scan_result, create_whatsapp_response

router = APIRouter()


@router.post("/scan", response_model=ScanResponse)
def scan_text(request: ScanRequest, db: Session = Depends(get_db)):
    """
    Main endpoint - takes text input and returns AI analysis.
    Also saves the result to the database for history tracking.
    """
    # send text to groq AI for analysis
    result = analyze_text(request.text, request.analysis_type)

    # save result to mysql database
    scan = ScanResult(
        input_text=request.text,
        analysis_type=request.analysis_type,
        verdict=result["verdict"],
        confidence_score=result["confidence_score"],
        explanation=result["explanation"],
        risk_indicators=result["risk_indicators"],
        source="web",
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan


@router.get("/history", response_model=list[ScanResponse])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    """Returns the most recent scan results (default 20)"""
    results = (
        db.query(ScanResult)
        .order_by(ScanResult.created_at.desc())
        .limit(limit)
        .all()
    )
    return results


@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Returns overall statistics for the dashboard cards"""
    total = db.query(ScanResult).count()

    fake_count = (
        db.query(ScanResult)
        .filter(ScanResult.verdict.in_(["FAKE", "SCAM", "SUSPICIOUS"]))
        .count()
    )
    safe_count = (
        db.query(ScanResult)
        .filter(ScanResult.verdict.in_(["REAL", "SAFE"]))
        .count()
    )

    # calculate threat percentage (avoid division by zero)
    if total > 0:
        threat_rate = round(fake_count / total * 100, 1)
    else:
        threat_rate = 0

    return {
        "total_scans": total,
        "threats_detected": fake_count,
        "safe_content": safe_count,
        "threat_rate": threat_rate,
    }


@router.post("/whatsapp/webhook", response_class=PlainTextResponse)
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Twilio sends a POST request here whenever someone messages our WhatsApp number.
    We analyze the message and send back the result.
    """
    form_data = await request.form()
    body = form_data.get("Body", "").strip()
    from_number = form_data.get("From", "")

    # if empty message, send welcome text
    if not body:
        return create_whatsapp_response(
            "Welcome to TruthScan AI!\n\n"
            "Send me any news headline, message, or claim "
            "and I'll analyze it for fake news or scams."
        )

    # try to auto-detect what type of content this is
    analysis_type = "news"
    lower_text = body.lower()

    # check if it looks like a URL
    if any(keyword in lower_text for keyword in ["http://", "https://", "www.", ".com", ".org"]):
        analysis_type = "url"
    # check if it looks like a scam message
    elif any(keyword in lower_text for keyword in [
        "won", "prize", "lottery", "click here", "urgent",
        "account", "verify", "suspended", "congrat"
    ]):
        analysis_type = "scam"

    # run AI analysis
    result = analyze_text(body, analysis_type)

    # save to database
    scan = ScanResult(
        input_text=body,
        analysis_type=analysis_type,
        verdict=result["verdict"],
        confidence_score=result["confidence_score"],
        explanation=result["explanation"],
        risk_indicators=result["risk_indicators"],
        source="whatsapp",
        user_phone=from_number,
    )
    db.add(scan)
    db.commit()

    # format and send response back to whatsapp
    response_text = format_scan_result(result)
    return create_whatsapp_response(response_text)

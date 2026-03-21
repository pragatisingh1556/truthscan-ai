"""
WhatsApp Integration using Twilio API
Handles incoming messages from WhatsApp and sends back scan results
"""

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
import json


def get_twilio_client():
    """Create a Twilio client instance"""
    return Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def format_scan_result(result):
    """
    Formats the AI scan result into a nice WhatsApp message
    with emojis and a visual confidence bar
    """
    verdict = result["verdict"]
    confidence = result["confidence_score"]
    explanation = result["explanation"]

    # build a simple text-based progress bar for confidence
    filled = round(confidence * 10)
    bar = "=" * filled + "-" * (10 - filled)

    # add risk indicators if there are any
    indicators = ""
    if result.get("risk_indicators"):
        try:
            risks = json.loads(result["risk_indicators"])
            if risks:
                indicators = "\n\n*Risk Indicators:*\n"
                for r in risks:
                    indicators += f"  - {r}\n"
        except (json.JSONDecodeError, TypeError):
            pass

    msg = f"""*TruthScan AI Result*

*Verdict:* {verdict}
*Confidence:* [{bar}] {confidence:.0%}

*Analysis:*
{explanation}{indicators}
---
Send any text, news, or message to scan it!"""

    return msg


def create_whatsapp_response(message):
    """Create a TwiML response that Twilio understands"""
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)


def send_whatsapp_message(to, body):
    """Send a WhatsApp message to a specific number"""
    client = get_twilio_client()
    message = client.messages.create(
        body=body,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to,
    )
    return message.sid

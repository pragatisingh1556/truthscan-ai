"""
Database models - defines the table structure for storing scan results
"""

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ScanResult(Base):
    """
    Stores every scan that users perform.
    Each row = one text that was analyzed for fake news or scam.
    """
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    input_text = Column(Text, nullable=False)            # the text user submitted
    analysis_type = Column(String(20), nullable=False, default="news")  # news/scam/url/message
    verdict = Column(String(50), nullable=False)          # FAKE, REAL, SCAM, SAFE, SUSPICIOUS
    confidence_score = Column(Float, nullable=False)      # 0.0 to 1.0
    explanation = Column(Text, nullable=False)            # AI's reasoning
    risk_indicators = Column(Text, nullable=True)         # stored as JSON string
    source = Column(String(20), default="web")            # web or whatsapp
    user_phone = Column(String(30), nullable=True)        # only for whatsapp users
    created_at = Column(DateTime(timezone=True), server_default=func.now())

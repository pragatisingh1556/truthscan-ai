"""
Pydantic schemas for request validation and response formatting
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScanRequest(BaseModel):
    """What the user sends to the /scan endpoint"""
    text: str
    analysis_type: str = "news"  # can be: news, scam, url, message


class ScanResponse(BaseModel):
    """What we send back after analyzing the text"""
    id: int
    input_text: str
    analysis_type: str
    verdict: str
    confidence_score: float
    explanation: str
    risk_indicators: Optional[str] = None
    source: str
    created_at: datetime

    # this lets pydantic read data directly from SQLAlchemy model objects
    model_config = {"from_attributes": True}

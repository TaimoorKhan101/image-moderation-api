from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class CategoryScore(BaseModel):
    """Score for a specific moderation category"""
    category: str = Field(..., description="Moderation category name")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score between 0 and 1")


class ModerationResult(BaseModel):
    """Final moderation response"""
    is_safe: bool = Field(..., description="Whether the image passed safety thresholds")
    scores: List[CategoryScore] = Field(..., description="List of category scores")
    filename: str = Field(..., description="Original filename of the uploaded image")
    content_type: str = Field(..., description="MIME type of the uploaded image")

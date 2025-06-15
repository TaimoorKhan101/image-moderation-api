from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field
from app.models import PyObjectId  # ✅ Reuse the shared ObjectId model
from bson import ObjectId


class UsageModel(BaseModel):
    """Usage tracking model for MongoDB"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    token: str = Field(..., description="Bearer token used for the request")
    endpoint: str = Field(..., description="API endpoint accessed")
    method: str = Field(..., description="HTTP method used")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request timestamp")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    request_size: Optional[int] = Field(None, description="Request payload size in bytes")
    response_status: Optional[int] = Field(None, description="HTTP response status code")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        populate_by_name = True  # ✅ Replaces allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {  # ✅ Replaces schema_extra
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "endpoint": "/moderate",
                "method": "POST",
                "timestamp": "2024-01-01T12:00:00",
                "ip_address": "192.168.1.1",
                "user_agent": "Mozilla/5.0...",
                "request_size": 1024,
                "response_status": 200,
                "response_time": 150.5,
                "metadata": {"image_format": "jpeg", "file_size": 2048}
            }
        }


class UsageCreate(BaseModel):
    """Usage creation model"""
    token: str = Field(..., description="Bearer token used for the request")
    endpoint: str = Field(..., description="API endpoint accessed")
    method: str = Field(..., description="HTTP method used")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    request_size: Optional[int] = Field(None, description="Request payload size in bytes")
    response_status: Optional[int] = Field(None, description="HTTP response status code")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class UsageResponse(BaseModel):
    """Usage response model"""
    id: str = Field(..., description="Usage record ID")
    token: str = Field(..., description="Bearer token used for the request")
    endpoint: str = Field(..., description="API endpoint accessed")
    method: str = Field(..., description="HTTP method used")
    timestamp: datetime = Field(..., description="Request timestamp")
    ip_address: Optional[str] = Field(None, description="Client IP address")
    user_agent: Optional[str] = Field(None, description="Client user agent")
    request_size: Optional[int] = Field(None, description="Request payload size in bytes")
    response_status: Optional[int] = Field(None, description="HTTP response status code")
    response_time: Optional[float] = Field(None, description="Response time in milliseconds")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class UsageStats(BaseModel):
    """Usage statistics model"""
    total_requests: int = Field(..., description="Total number of requests")
    unique_tokens: int = Field(..., description="Number of unique tokens")
    endpoints_usage: Dict[str, int] = Field(..., description="Usage count per endpoint")
    daily_usage: Dict[str, int] = Field(..., description="Daily usage counts")
    average_response_time: Optional[float] = Field(None, description="Average response time in ms")

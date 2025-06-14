from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class TokenModel(BaseModel):
    """Token model for MongoDB"""
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    token: str = Field(..., description="Bearer token string")
    is_admin: bool = Field(default=False, description="Admin privileges flag")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Token creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
    is_active: bool = Field(default=True, description="Token active status")
    description: Optional[str] = Field(None, description="Token description or purpose")
    created_by: Optional[str] = Field(None, description="Token creator identifier")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "is_admin": False,
                "created_at": "2024-01-01T00:00:00",
                "expires_at": "2024-12-31T23:59:59",
                "is_active": True,
                "description": "API token for user authentication",
                "created_by": "admin"
            }
        }

class TokenCreate(BaseModel):
    """Token creation request model"""
    is_admin: bool = Field(default=False, description="Admin privileges flag")
    expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
    description: Optional[str] = Field(None, description="Token description or purpose")

class TokenResponse(BaseModel):
    """Token response model"""
    id: str = Field(..., description="Token ID")
    token: str = Field(..., description="Bearer token string")
    is_admin: bool = Field(..., description="Admin privileges flag")
    created_at: datetime = Field(..., description="Token creation timestamp")
    expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
    is_active: bool = Field(..., description="Token active status")
    description: Optional[str] = Field(None, description="Token description or purpose")

class TokenUpdate(BaseModel):
    """Token update model"""
    is_active: Optional[bool] = Field(None, description="Token active status")
    description: Optional[str] = Field(None, description="Token description or purpose")
    expires_at: Optional[datetime] = Field(None, description="Token expiration timestamp")
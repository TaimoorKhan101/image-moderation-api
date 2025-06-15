from datetime import datetime
from typing import Optional, Any, Callable

from bson import ObjectId
from pydantic import BaseModel, Field
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic v2"""
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Callable) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.no_info_after_validator_function(
                cls.validate,
                core_schema.str_schema()
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


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
        populate_by_name = True  # replaces allow_population_by_field_name
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {  # replaces schema_extra
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

class TokenInfo(BaseModel):
    """Read-only metadata about an issued token (excluding the token value)"""
    token_id: str = Field(..., description="Token document ID")
    isAdmin: bool = Field(..., description="Admin privileges flag")
    createdAt: datetime = Field(..., description="Token creation time")
    description: Optional[str] = Field(None, description="Token description")
    lastUsed: Optional[datetime] = Field(None, description="Last time this token was used")
    usageCount: int = Field(default=0, description="Total usage count")

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

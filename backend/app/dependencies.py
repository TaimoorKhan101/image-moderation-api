from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any

from app.core.security import verify_token, verify_admin_token
from app.services.auth_service import AuthService
from app.services.moderation_service import ModerationService
from app.services.usage_service import UsageService

# Security scheme
security = HTTPBearer()

# Service dependencies
def get_auth_service() -> AuthService:
    """Get authentication service instance."""
    return AuthService()

def get_moderation_service() -> ModerationService:
    """Get moderation service instance."""
    return ModerationService()

def get_usage_service() -> UsageService:
    """Get usage tracking service instance."""
    return UsageService()

# Authentication dependencies
async def get_current_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Extract and return the current bearer token.
    """
    return credentials.credentials

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Get current authenticated user information.
    Validates token and returns user data.
    """
    try:
        token_data = await verify_token(credentials.credentials)
        return token_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_admin_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    Get current authenticated admin user.
    Validates token and ensures admin privileges.
    """
    try:
        admin_data = await verify_admin_token(credentials.credentials)
        return admin_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Optional dependencies for services with error handling
async def get_auth_service_optional() -> AuthService:
    """Get auth service with error handling."""
    try:
        return AuthService()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )

async def get_moderation_service_optional() -> ModerationService:
    """Get moderation service with error handling."""
    try:
        return ModerationService()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Moderation service unavailable"
        )
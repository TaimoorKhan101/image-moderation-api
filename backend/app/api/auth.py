from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
import logging

from app.core.security import verify_admin_token, get_current_user
from app.services.auth_service import AuthService
from app.models.token import TokenCreate, TokenResponse, TokenInfo
from app.core.exceptions import CustomException

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Dependency to get auth service
def get_auth_service() -> AuthService:
    return AuthService()

@router.post("/tokens", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def create_token(
    token_data: TokenCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Create a new bearer token (Admin only).
    
    - **isAdmin**: Whether the token has admin privileges
    - **description**: Optional description for the token
    """
    try:
        # Verify admin privileges
        current_user = await verify_admin_token(credentials.credentials)
        
        # Create new token
        new_token = await auth_service.create_token(
            is_admin=token_data.isAdmin,
            description=token_data.description
        )
        
        logger.info(f"Admin {current_user['token'][:8]}... created new token")
        
        return TokenResponse(
            token=new_token["token"],
            isAdmin=new_token["isAdmin"],
            createdAt=new_token["createdAt"],
            description=new_token.get("description")
        )
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Error creating token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create token"
        )

@router.get("/tokens", response_model=List[TokenInfo])
async def get_all_tokens(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Get all issued tokens (Admin only).
    
    Returns a list of all tokens with their metadata (excluding the actual token values).
    """
    try:
        # Verify admin privileges
        current_user = await verify_admin_token(credentials.credentials)
        
        # Get all tokens
        tokens = await auth_service.get_all_tokens()
        
        logger.info(f"Admin {current_user['token'][:8]}... retrieved token list")
        
        return [
            TokenInfo(
                token_id=token["_id"],
                isAdmin=token["isAdmin"],
                createdAt=token["createdAt"],
                description=token.get("description"),
                lastUsed=token.get("lastUsed"),
                usageCount=token.get("usageCount", 0)
            )
            for token in tokens
        ]
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving tokens: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tokens"
        )

@router.delete("/tokens/{token}")
async def delete_token(
    token: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Delete a specific token (Admin only).
    
    - **token**: The token to delete
    """
    try:
        # Verify admin privileges
        current_user = await verify_admin_token(credentials.credentials)
        
        # Prevent admin from deleting their own token
        if token == current_user["token"]:
            raise CustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own token",
                error_type="SELF_TOKEN_DELETE"
            )
        
        # Delete token
        deleted = await auth_service.delete_token(token)
        
        if not deleted:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Token not found",
                error_type="TOKEN_NOT_FOUND"
            )
        
        logger.info(f"Admin {current_user['token'][:8]}... deleted token {token[:8]}...")
        
        return {"message": "Token deleted successfully"}
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Error deleting token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete token"
        )
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging

from app.core.security import get_current_user
from app.services.moderation_service import ModerationService
from app.models.moderation import ModerationResult
from app.utils.file_handler import validate_file
from app.core.exceptions import CustomException

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

# Dependency to get moderation service
def get_moderation_service() -> ModerationService:
    return ModerationService()

@router.post("/moderate", response_model=ModerationResult)
async def moderate_image(
    file: UploadFile = File(...),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    moderation_service: ModerationService = Depends(get_moderation_service)
):
    """
    Moderate an uploaded image for harmful content.
    
    - **file**: Image file to analyze (jpg, jpeg, png, gif, webp)
    
    Returns a detailed safety report with confidence scores for each category.
    """
    try:
        # Verify valid token (any authenticated user can access)
        current_user = await get_current_user(credentials.credentials)
        
        # Validate uploaded file
        await validate_file(file)
        
        # Read file content
        file_content = await file.read()
        
        # Reset file position for potential reuse
        await file.seek(0)
        
        # Perform moderation analysis
        result = await moderation_service.analyze_image(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type
        )
        
        logger.info(
            f"Image moderation completed for user {current_user['token'][:8]}... "
            f"File: {file.filename}, Safe: {result.is_safe}"
        )
        
        return result
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Error during image moderation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process image"
        )

@router.get("/moderate/categories")
async def get_moderation_categories(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get available moderation categories and their descriptions.
    
    Returns information about what types of content are detected.
    """
    try:
        # Verify valid token
        await get_current_user(credentials.credentials)
        
        categories = {
            "explicit_nudity": {
                "name": "Explicit Nudity",
                "description": "Sexually explicit content and nudity",
                "severity": "high"
            },
            "graphic_violence": {
                "name": "Graphic Violence", 
                "description": "Violent, gory, or disturbing imagery",
                "severity": "high"
            },
            "hate_symbols": {
                "name": "Hate Symbols",
                "description": "Hate speech symbols and extremist imagery",
                "severity": "high"
            },
            "self_harm": {
                "name": "Self Harm",
                "description": "Content depicting self-harm or suicide",
                "severity": "high"
            },
            "spam_unwanted": {
                "name": "Spam/Unwanted",
                "description": "Spam, advertisements, or unwanted content",
                "severity": "medium"
            }
        }
        
        return {
            "categories": categories,
            "confidence_threshold": 0.7,
            "supported_formats": ["jpg", "jpeg", "png", "gif", "webp"],
            "max_file_size": "10MB"
        }
        
    except CustomException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )
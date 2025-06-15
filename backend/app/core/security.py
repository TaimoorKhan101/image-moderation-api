# backend/app/core/security.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.database import get_tokens_collection
from app.core.exceptions import CustomException

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    tokens_collection = get_tokens_collection()

    token_doc = await tokens_collection.find_one({"token": token})
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token_doc


async def verify_admin_token(
    token_str: str
):
    tokens_collection = get_tokens_collection()

    token_doc = await tokens_collection.find_one({"token": token_str})
    if not token_doc:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not token_doc.get("isAdmin"):
        raise HTTPException(status_code=403, detail="Admin privileges required")

    return token_doc

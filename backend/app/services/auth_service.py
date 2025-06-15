# backend/app/services/auth_service.py

import secrets
from datetime import datetime
from app.core.database import get_tokens_collection

class AuthService:
    async def create_token(self, is_admin: bool, description: str = None):
        token_value = secrets.token_urlsafe(32)

        token_doc = {
            "token": token_value,
            "isAdmin": is_admin,
            "description": description,
            "createdAt": datetime.utcnow(),
            "usageCount": 0,
        }

        tokens_collection = get_tokens_collection()
        await tokens_collection.insert_one(token_doc)
        return token_doc

    async def get_all_tokens(self):
        tokens_collection = get_tokens_collection()
        return await tokens_collection.find({}, {"token": 0}).to_list(length=100)

    async def delete_token(self, token: str):
        tokens_collection = get_tokens_collection()
        result = await tokens_collection.delete_one({"token": token})
        return result.deleted_count > 0

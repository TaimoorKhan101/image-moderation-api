# backend/app/services/usage_services.py

from app.core.database import get_usages_collection
from app.models.usage import UsageCreate
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UsageService:
    @property
    def collection(self):
        return get_usages_collection()

    async def log_usage(self, usage: UsageCreate):
        """Log API usage into MongoDB"""
        try:
            usage_doc = usage.dict()
            usage_doc["timestamp"] = datetime.utcnow()
            await self.collection.insert_one(usage_doc)
        except Exception as e:
            logger.warning(f"Failed to log usage: {e}")

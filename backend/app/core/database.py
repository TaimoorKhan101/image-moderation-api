from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from app.config import settings

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    database = None

# Global database instance
db_instance = Database()

async def connect_to_mongo():
    """Create database connection"""
    try:
        db_instance.client = AsyncIOMotorClient(
            settings.mongodb_url,
            maxPoolSize=10,
            minPoolSize=5,
            serverSelectionTimeoutMS=5000,
        )
        
        # Test the connection
        await db_instance.client.admin.command('ping')
        
        db_instance.database = db_instance.client[settings.database_name]
        
        # Create indexes for better performance
        await create_indexes()
        
        logger.info("Connected to MongoDB Atlas successfully")
        
    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        raise

async def close_mongo_connection():
    """Close database connection"""
    if db_instance.client:
        db_instance.client.close()
        logger.info("Disconnected from MongoDB")

async def create_indexes():
    """Create database indexes for performance optimization"""
    try:
        # Index for tokens collection
        await db_instance.database.tokens.create_index("token", unique=True)
        await db_instance.database.tokens.create_index("createdAt")
        
        # Index for usages collection
        await db_instance.database.usages.create_index([("token", 1), ("timestamp", -1)])
        await db_instance.database.usages.create_index("endpoint")
        
        logger.info("Database indexes created successfully")
        
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")

def get_database():
    """Get database instance"""
    return db_instance.database

# Collections shortcuts
def get_tokens_collection():
    return db_instance.database.tokens

def get_usages_collection():
    return db_instance.database.usages
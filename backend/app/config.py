from pydantic_settings import BaseSettings
from pydantic import BaseSettings
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Configuration
    """
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 7000
    ENVIRONMENT: str = "development"
    """
    # Security
    """
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    """
    # MongoDB Atlas Configuration
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb+srv://username:password@cluster.mongodb.net/")
    database_name: str = os.getenv("DATABASE_NAME", "image_moderation")
    
    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    algorithm: str = "HS256"
    
    # Application Configuration
    app_name: str = "Image Moderation API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "7000"))
    # File Upload Configuration
    """
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "gif", "webp"]
    UPLOAD_DIRECTORY: str = "uploads"
    """

    # CORS Configuration
    """
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    """

    # Rate Limiting
    """
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 3600  # 1 hour in seconds
    """

    # Moderation Configuration
    """
    CONFIDENCE_THRESHOLD: float = 0.7
    MODERATION_CATEGORIES: List[str] = [
        "explicit_nudity",
        "graphic_violence", 
        "hate_symbols",
        "self_harm",
        "spam_unwanted"
    ]
    """
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure upload directory exists
"""
os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
"""
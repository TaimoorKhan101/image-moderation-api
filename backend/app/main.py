from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging

from app.config import settings
from app.core.database import connect_to_mongo, close_mongo_connection
from app.core.exceptions import CustomException
from app.api import auth, moderation
from app.api.middleware import UsageTrackingMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="Image Moderation API",
    description="API for moderating images and detecting harmful content",
    version="1.0.0",
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.ENVIRONMENT == "development" else settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom usage tracking middleware
app.add_middleware(UsageTrackingMiddleware)

# Add timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Custom exception handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "type": exc.error_type}
    )

# Database connection events
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up Image Moderation API...")
    await connect_to_mongo()
    logger.info("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down Image Moderation API...")
    await close_mongo_connection()
    logger.info("Disconnected from MongoDB")

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Image Moderation API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs" if settings.ENVIRONMENT == "development" else "disabled"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT
    }

# Include routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

app.include_router(
    moderation.router,
    prefix="",
    tags=["moderation"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.ENVIRONMENT == "development"
    )
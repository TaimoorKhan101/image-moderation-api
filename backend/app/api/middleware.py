from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging
from typing import Optional

from app.services.usage_services import UsageService
from app.core.database import get_database

logger = logging.getLogger(__name__)

class UsageTrackingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to track API usage per token.
    Records each API call with timestamp and endpoint information.
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.usage_service = UsageService()
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Extract token from Authorization header
        token = self._extract_token(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Track usage if token is present and request was successful
        if token and response.status_code < 400:
            try:
                await self._track_usage(
                    token=token,
                    endpoint=str(request.url.path),
                    method=request.method,
                    status_code=response.status_code,
                    process_time=process_time,
                    user_agent=request.headers.get("user-agent"),
                    ip_address=self._get_client_ip(request)
                )
            except Exception as e:
                # Don't let usage tracking errors affect the main response
                logger.error(f"Error tracking usage: {str(e)}")
        
        return response
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """Extract bearer token from Authorization header."""
        try:
            auth_header = request.headers.get("authorization")
            if auth_header and auth_header.startswith("Bearer "):
                return auth_header.split(" ")[1]
        except Exception:
            pass
        return None
    
    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address from request."""
        # Check for forwarded headers first (for proxy/load balancer scenarios)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fallback to direct client IP
        if hasattr(request, "client") and request.client:
            return request.client.host
        
        return "unknown"
    
    async def _track_usage(
        self,
        token: str,
        endpoint: str,
        method: str,
        status_code: int,
        process_time: float,
        user_agent: Optional[str] = None,
        ip_address: str = "unknown"
    ):
        """Record usage information in the database."""
        try:
            await self.usage_service.record_usage(
                token=token,
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                process_time=process_time,
                user_agent=user_agent,
                ip_address=ip_address
            )
            
            # Update token's last used timestamp
            await self.usage_service.update_token_last_used(token)
            
        except Exception as e:
            logger.error(f"Failed to track usage for token {token[:8]}...: {str(e)}")
            raise
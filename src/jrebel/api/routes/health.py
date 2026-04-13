"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    service: str = "jrebel-license-server"
    version: str = "2.0.0"


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for monitoring."""
    return HealthResponse()

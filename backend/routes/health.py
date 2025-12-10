"""
Health check endpoint
Returns status of all services
"""

from fastapi import APIRouter, status
from datetime import datetime

from backend.schemas import HealthCheckResponse
from backend.database import engine
from backend.services.rag_service import rag_service
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check health status of all services (database, Qdrant, OpenAI)"
)
async def health_check():
    """
    Health check endpoint

    Returns the health status of:
    - Database (Neon PostgreSQL)
    - Qdrant vector database
    - OpenAI API

    No authentication required
    """
    services_status = {}

    # Check database
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        services_status["database"] = "ok"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        services_status["database"] = "error"

    # Check RAG service dependencies (Qdrant + OpenAI)
    try:
        rag_health = await rag_service.health_check()
        services_status["qdrant"] = rag_health["qdrant"]
        services_status["openai"] = rag_health["openai"]
    except Exception as e:
        logger.error(f"RAG service health check failed: {e}")
        services_status["qdrant"] = "error"
        services_status["openai"] = "error"

    # Determine overall status
    all_healthy = all(status == "ok" for status in services_status.values())
    overall_status = "healthy" if all_healthy else "degraded"

    # Build response
    response = HealthCheckResponse(
        status=overall_status,
        timestamp=datetime.utcnow(),
        services=services_status,
        message=None if all_healthy else "Some services are experiencing issues"
    )

    # Return appropriate status code
    response_status = status.HTTP_200_OK if all_healthy else status.HTTP_503_SERVICE_UNAVAILABLE

    return response

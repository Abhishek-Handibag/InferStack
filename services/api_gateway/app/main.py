from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from services.api_gateway.app.core.config import get_settings
from services.api_gateway.app.database.connection import get_db_session


# Load application configuration.
settings = get_settings()


# Create the FastAPI application.
app = FastAPI(
    title=settings.app_name,
    description="Enterprise AI Engineering Platform",
    version=settings.app_version,
)


@app.get(f"{settings.api_prefix}/health")
async def health_check():
    """
    Basic liveness check.

    This only verifies that the API process itself is running.
    """

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


@app.get(f"{settings.api_prefix}/health/ready")
async def readiness_check(
    db: AsyncSession = Depends(get_db_session),
):
    """
    Readiness check.

    This verifies that the API can communicate with PostgreSQL.
    """

    await db.execute(text("SELECT 1"))

    return {
        "status": "ready",
        "database": "connected",
    }
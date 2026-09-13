from fastapi import FastAPI

from services.api_gateway.app.core.config import get_settings

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
    Basic health-check endpoint.

    This confirms that the API Gateway is running.
    """

    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
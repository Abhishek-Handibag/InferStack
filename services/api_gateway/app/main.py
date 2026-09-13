from fastapi import FastAPI


# Create the main FastAPI application.
app = FastAPI(
    title="InferStack API",
    description="Enterprise AI Engineering Platform",
    version="0.1.0",
)


@app.get("/api/v1/health")
async def health_check():
    """
    Basic health-check endpoint.

    This endpoint confirms that the API Gateway
    is running and able to accept requests.
    """

    return {
        "status": "healthy",
        "service": "inferstack-api",
        "version": "0.1.0",
    }
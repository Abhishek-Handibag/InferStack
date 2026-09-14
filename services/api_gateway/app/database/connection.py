from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.api_gateway.app.core.config import get_settings


# Load application configuration.
settings = get_settings()


# Create the asynchronous SQLAlchemy engine.
#
# The engine manages the connection pool used to communicate
# with PostgreSQL.
engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
)


# Create a factory for asynchronous database sessions.
#
# Each request that needs the database can obtain a session
# from this factory.
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session to FastAPI dependencies.

    The session is automatically closed after the request
    finishes.
    """

    async with AsyncSessionLocal() as session:
        yield session
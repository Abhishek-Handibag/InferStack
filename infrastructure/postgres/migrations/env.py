from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from services.api_gateway.app.core.config import get_settings
from services.api_gateway.app.database.models import Base


# Alembic configuration object.
config = context.config


# Configure Python logging using alembic.ini.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Import our SQLAlchemy metadata.
#
# Alembic uses this metadata to detect changes between
# our Python models and the actual PostgreSQL schema.
target_metadata = Base.metadata


# Load application settings.
settings = get_settings()


def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.

    This mode generates SQL statements instead of directly
    executing them against PostgreSQL.
    """

    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """
    Configure Alembic using an active database connection.
    """

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Create an asynchronous SQLAlchemy engine and run migrations.
    """

    connectable = async_engine_from_config(
        {
            "sqlalchemy.url": settings.database_url,
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Run migrations against the live PostgreSQL database.
    """

    import asyncio

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
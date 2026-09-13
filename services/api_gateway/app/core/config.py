from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration.

    Values are loaded from environment variables and the
    local .env file.

    Keeping configuration in one place makes it easier to
    run InferStack across development, testing, staging,
    and production environments.
    """

    # Application settings
    app_name: str = "InferStack API"
    app_version: str = "0.1.0"
    environment: str = "development"

    # API settings
    api_prefix: str = "/api/v1"

    # Database settings
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/inferstack"

    # Redis settings
    redis_url: str = "redis://localhost:6379/0"

    # Load configuration from .env.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.

    Caching ensures that we don't repeatedly parse the
    environment variables every time configuration is requested.
    """
    return Settings()
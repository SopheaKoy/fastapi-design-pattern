# app/infrastructure/config/settings.py

from pydantic_settings import BaseSettings
from decouple import config


class Settings(BaseSettings):
    """Application settings"""
    # Database
    database_url: str = config(
        "DATABASE_URL",
        default="postgresql+asyncpg://user:password@localhost:5432/fastapi_db"
    )
    sql_echo: bool = config("SQL_ECHO", default=False, cast=bool)

    # Redis
    redis_url: str = config(
        "REDIS_URL",
        default="redis://localhost:6379"
    )

    # App
    app_name: str = config("APP_NAME", default="FastAPI DDD Pattern")
    debug: bool = config("DEBUG", default=False, cast=bool)
    log_level: str = config("LOG_LEVEL", default="INFO")

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

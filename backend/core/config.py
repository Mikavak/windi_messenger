from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Теперь нужно добавить аннотации типов для всех атрибутов
    DATABASE_URL: str = 'postgresql+asyncpg://postgres:9078@localhost:5432/windi_messenger'
    # Остальные настройки с аннотациями типов
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Настройки приложения
    PROJECT_NAME: str = "WinDI Messenger"
    API_V1_PREFIX: str = "/api"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
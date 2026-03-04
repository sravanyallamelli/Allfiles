from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

    PROJECT_NAME: str = "Attendance Management API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str
    BACKEND_CORS_ORIGINS: str = "http://localhost:5173"
    LATE_CHECKIN_TIME: str = "09:15"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

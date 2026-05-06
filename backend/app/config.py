from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Curso de Python GDG Guadalajara x CUGDL"
    app_env: str = "dev"
    backend_cors_origins: List[str] = ["http://localhost:5173"]

    jwt_secret: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    google_client_id: str | None = None
    allow_dev_email_login: bool = True
    allowed_email_domains: List[str] = ["estudiantes.udg.mx", "alumnos.udg.mx"]

    supabase_url: str | None = None
    supabase_key: str | None = None

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return value
        return [item.strip() for item in value.split(",") if item.strip()]

    @field_validator("allowed_email_domains", mode="before")
    @classmethod
    def parse_domains(cls, value: str | List[str]) -> List[str]:
        if isinstance(value, list):
            return [item.strip().lower().lstrip("@") for item in value if item.strip()]
        return [item.strip().lower().lstrip("@") for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


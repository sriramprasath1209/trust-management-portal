from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SUKI HOMES TRUST"
    database_url: str = "sqlite:///./trust_portal.db"
    secret_key: str = "change-this-secret-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 480

    # Allow both local development and your deployed Vercel frontend
    backend_cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173,https://trust-management-portal.vercel.app"
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.backend_cors_origins.split(",")
            if origin.strip()
        ]

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
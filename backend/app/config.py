from __future__ import annotations

import secrets
from functools import lru_cache
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["development", "test", "production"] = "development"
    database_url: str = "sqlite:///./dev.db"
    secret_key: str = ""
    access_token_minutes: int = 480
    cookie_secure: bool | None = None
    cors_origins: str = ""
    trust_proxy: bool = False
    anthropic_api_key: str = ""
    assistant_model: str = "claude-sonnet-5-5"
    seed_on_startup: bool = True
    auto_create_tables: bool | None = None

    @model_validator(mode="after")
    def _finalize(self) -> "Settings":
        if self.app_env == "production":
            if len(self.secret_key) < 32:
                raise ValueError("SECRET_KEY deve ter ao menos 32 caracteres em produção")
            if self.cookie_secure is None:
                self.cookie_secure = True
            if self.auto_create_tables is None:
                self.auto_create_tables = False
        else:
            if not self.secret_key:
                # Chave efêmera: as sessões deixam de valer a cada reinício em desenvolvimento.
                self.secret_key = secrets.token_urlsafe(48)
            if self.cookie_secure is None:
                self.cookie_secure = False
            if self.auto_create_tables is None:
                self.auto_create_tables = True
        return self

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def sqlalchemy_url(self) -> str:
        url = self.database_url
        for prefix in ("postgresql://", "postgres://"):
            if url.startswith(prefix):
                return "postgresql+psycopg://" + url[len(prefix):]
        return url

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

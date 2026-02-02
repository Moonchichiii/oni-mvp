from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from decouple import AutoConfig

BASE_DIR = Path(__file__).resolve().parents[2]
config = AutoConfig(search_path=str(BASE_DIR))


@dataclass(frozen=True)
class Settings:
    app_env: str
    public_base_url: str

    supabase_url: str
    supabase_anon_key: str | None
    supabase_service_role_key: str | None


def validate_settings(settings: Settings) -> None:
    if not settings.supabase_url:
        raise RuntimeError("Missing SUPABASE_URL in .env")

    if not (settings.supabase_service_role_key or settings.supabase_anon_key):
        raise RuntimeError(
            "Missing SUPABASE_SERVICE_ROLE_KEY and SUPABASE_ANON_KEY "
            "(set at least one)."
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings(
        app_env=config("APP_ENV", default="dev"),
        public_base_url=config("PUBLIC_BASE_URL", default="http://127.0.0.1:8000"),
        supabase_url=config("SUPABASE_URL", default=""),
        supabase_anon_key=config("SUPABASE_ANON_KEY", default=None),
        supabase_service_role_key=config("SUPABASE_SERVICE_ROLE_KEY", default=None),
    )
    validate_settings(settings)
    return settings

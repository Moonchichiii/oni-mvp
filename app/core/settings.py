from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from decouple import AutoConfig

BASE_DIR = Path(__file__).resolve().parents[2]
config = AutoConfig(search_path=str(BASE_DIR))


@dataclass(frozen=True)
class Settings:
    app_env: str
    app_secret: str
    public_base_url: str

    supabase_url: str
    supabase_anon_key: str | None
    supabase_service_role_key: str | None


def get_settings() -> Settings:
    return Settings(
        app_env=config("APP_ENV", default="dev"),
        app_secret=config("APP_SECRET", default="change-me"),
        public_base_url=config("PUBLIC_BASE_URL", default="http://127.0.0.1:8000"),
        supabase_url=config("SUPABASE_URL", default=""),
        supabase_anon_key=config("SUPABASE_ANON_KEY", default=None),
        supabase_service_role_key=config("SUPABASE_SERVICE_ROLE_KEY", default=None),
    )

    def validate_settings(settings: Settings) -> None:
        """Validate that required settings are present."""
        if not settings.supabase_url:
            raise RuntimeError(
                "Missing SUPABASE_URL. "
                "Create a .env file (based on .env.example) with Supabase credentials."
            )
        if not settings.supabase_anon_key:
            raise RuntimeError(
                "Missing SUPABASE_ANON_KEY. "
                "Create a .env file (based on .env.example) with Supabase credentials."
            )

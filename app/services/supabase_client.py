from supabase import Client, create_client

from app.core.settings import get_settings


def get_supabase_client() -> Client:
    settings = get_settings()

    key = settings.supabase_service_role_key or settings.supabase_anon_key

    if not key:
        raise RuntimeError(
            "Either SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY must be set"
        )

    return create_client(settings.supabase_url, key)

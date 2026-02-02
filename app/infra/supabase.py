from __future__ import annotations

from supabase import Client, create_client

from app.core.settings import get_settings


def get_supabase_client() -> Client:
    settings = get_settings()
    key = settings.supabase_service_role_key or settings.supabase_anon_key
    # validate_settings already guarantees one exists
    return create_client(settings.supabase_url, key)


def check_supabase_connection() -> bool:
    """
    Cheap sanity check: can we hit the API?
    Avoid printing secrets, only return True/False.
    """
    try:
        client = get_supabase_client()
        # tiny query; table exists in your project
        client.table("services").select("id").limit(1).execute()
        return True
    except Exception:
        return False

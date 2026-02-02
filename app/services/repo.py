from __future__ import annotations

from typing import Any

from postgrest.exceptions import APIError
from supabase import Client

from app.core.logging import log
from app.domain.models import Service, ServiceCreate
from app.services.errors import DuplicateServiceName, RepoUnavailable


def _is_unique_violation(exc: APIError) -> bool:
    """
    PostgREST surfaces Postgres errors; unique violation is SQLSTATE 23505.
    Depending on versions, it may appear as `exc.code` or in `exc.details`.
    """
    code: str | None = getattr(exc, "code", None)
    if code == "23505":
        return True

    details = getattr(exc, "details", None)
    if isinstance(details, str) and "23505" in details:
        return True

    return False


class ServicesRepo:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list_services(self) -> list[Service]:
        """Fetch all services ordered by creation date (newest first)."""
        try:
            resp = (
                self._client.table("services")
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
            data: list[dict[str, Any]] = resp.data or []
            return [Service.model_validate(row) for row in data]

        except Exception as exc:
            # list failures are infra-level: log + user-safe message
            log.exception("services.list_services failed")
            raise RepoUnavailable("Could not load services right now.") from exc

    def create_service(self, payload: ServiceCreate) -> Service:
        """Create a new service with the given name."""
        # NOTE: Pydantic already validates min_length=1.
        # Still strip for cleanliness and to avoid accidental whitespace duplicates.
        name = payload.name.strip()

        try:
            resp = (
                self._client.table("services")
                .insert({"name": name})
                .select("*")
                .single()
                .execute()
            )
            return Service.model_validate(resp.data)

        except APIError as exc:
            # Expected user behavior: do NOT log.exception for duplicates
            if _is_unique_violation(exc):
                raise DuplicateServiceName(
                    f'Service name "{name}" already exists.'
                ) from exc

            log.exception("services.create_service failed")
            raise RepoUnavailable("Service is unavailable right now.") from exc

        except Exception as exc:
            log.exception("services.create_service failed")
            raise RepoUnavailable("Could not save service right now.") from exc

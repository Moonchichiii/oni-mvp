from __future__ import annotations

from typing import Any

from postgrest.exceptions import APIError
from supabase import Client

from app.core.logging import log
from app.domain.models import Service, ServiceCreate
from app.services.errors import DuplicateServiceName, RepoUnavailable


class ServicesRepo:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list_services(self) -> list[Service]:
        """Fetch all services ordered by creation date."""
        try:
            resp = (
                self._client.table("services")
                .select("*")
                .order("created_at", desc=True)
                .execute()
            )
            data: list[dict[str, Any]] = resp.data or []
            return [Service.model_validate(row) for row in data]
        except APIError as exc:
            log.exception("services.list_services failed")
            raise RepoUnavailable("Could not load services right now.") from exc
        except Exception as exc:
            log.exception("services.list_services failed")
            raise RepoUnavailable("Could not load services right now.") from exc

    def create_service(self, payload: ServiceCreate) -> Service:
        """Create a new service with the given name."""
        name = payload.name.strip()
        if not name:
            raise RepoUnavailable("Invalid service name.")

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
            # Postgres unique violation (23505)
            if exc.code == "23505":
                raise DuplicateServiceName(
                    f'Service name "{name}" already exists.'
                ) from exc
            log.exception("services.create_service failed")
            raise RepoUnavailable("Service service is unavailable.") from exc
        except Exception as exc:
            log.exception("services.create_service failed")
            raise RepoUnavailable("Could not save service right now.") from exc

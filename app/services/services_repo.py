from __future__ import annotations

from typing import Any

from supabase import Client

from app.domain.models import Service, ServiceCreate


class ServicesRepo:
    def __init__(self, client: Client) -> None:
        self._client = client

    def list_services(self) -> list[Service]:
        resp = self._client.table("services").select("*").order("created_at").execute()

        data: list[dict[str, Any]] = resp.data or []
        return [Service.model_validate(row) for row in data]

    def create_service(self, payload: ServiceCreate) -> Service:
        resp = (
            self._client.table("services")
            .insert({"name": payload.name})
            .select("*")
            .single()
            .execute()
        )
        return Service.model_validate(resp.data)

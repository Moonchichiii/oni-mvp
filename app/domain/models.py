from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Service(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    name: str = Field(min_length=1, max_length=120)
    created_at: datetime


class ServiceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

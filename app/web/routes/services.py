from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.domain.models import ServiceCreate
from app.infra.supabase import get_supabase_client
from app.services.errors import DuplicateServiceName, RepoError
from app.services.repo import ServicesRepo
from app.web.templates import templates

router = APIRouter(prefix="/services", tags=["services"])


@router.get("", response_class=HTMLResponse)
def services_page(request: Request) -> HTMLResponse:
    repo = ServicesRepo(get_supabase_client())
    services = repo.list_services()
    return templates.TemplateResponse(
        "services/index.html",
        {"request": request, "services": services, "error": None},
    )


@router.post("/add", response_class=HTMLResponse)
def add_service(request: Request, name: str = Form(...)) -> HTMLResponse:
    repo = ServicesRepo(get_supabase_client())

    error: str | None = None
    try:
        payload = ServiceCreate(name=name.strip())
        repo.create_service(payload)
    except DuplicateServiceName as exc:
        error = exc.message
    except RepoError as exc:
        error = exc.message

    services = repo.list_services()

    return templates.TemplateResponse(
        "services/_add_result.html",
        {"request": request, "services": services, "error": error},
    )

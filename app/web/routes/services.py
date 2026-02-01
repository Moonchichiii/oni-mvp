from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.domain.models import ServiceCreate
from app.services.services_repo import ServicesRepo
from app.services.supabase_client import get_supabase_client

router = APIRouter(prefix="/services", tags=["services"])

BASE_DIR = Path(__file__).resolve().parents[2]
templates = Jinja2Templates(directory=str(BASE_DIR / "web" / "templates"))


@router.get("", response_class=HTMLResponse)
def services_page(request: Request) -> HTMLResponse:
    repo = ServicesRepo(get_supabase_client())
    services = repo.list_services()
    return templates.TemplateResponse(
        "services/index.html",
        {"request": request, "services": services},
    )


@router.post("/add", response_class=HTMLResponse)
def add_service(name: str = Form(...)) -> HTMLResponse:
    repo = ServicesRepo(get_supabase_client())

    payload = ServiceCreate(name=name.strip())
    repo.create_service(payload)

    # Return the refreshed list fragment for HTMX
    services = repo.list_services()
    return templates.TemplateResponse(
        "services/_list.html",
        {"request": None, "services": services},
    )

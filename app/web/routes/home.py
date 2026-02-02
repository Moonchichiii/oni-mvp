from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.web.templates import templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})

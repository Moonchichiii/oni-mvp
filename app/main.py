from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.web.routes.home import router as home_router
from app.web.routes.services import router as services_router

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web" / "static"

app = FastAPI()

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(home_router)
app.include_router(services_router)

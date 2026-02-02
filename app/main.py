from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.core.logging import configure_logging, log
from app.core.paths import STATIC_DIR
from app.core.settings import get_settings
from app.infra.supabase import check_supabase_connection
from app.web.routes.health import router as health_router
from app.web.routes.home import router as home_router
from app.web.routes.services import router as services_router


def create_app() -> FastAPI:
    configure_logging()

    settings = get_settings()
    sb_ok = check_supabase_connection()

    log.info("startup env=%s", settings.app_env)
    log.info("startup supabase_connected=%s", sb_ok)

    app = FastAPI()

    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon() -> FileResponse:
        return FileResponse(STATIC_DIR / "favicon.ico")

    app.include_router(health_router)
    app.include_router(home_router)
    app.include_router(services_router)

    return app


app = create_app()

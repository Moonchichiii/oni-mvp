from __future__ import annotations

from pathlib import Path

from fastapi.templating import Jinja2Templates

APP_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = APP_DIR / "web" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

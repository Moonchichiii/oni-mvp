from __future__ import annotations

from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
WEB_DIR = APP_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"

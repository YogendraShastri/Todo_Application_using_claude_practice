from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import pages, todos
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_title)
    app.include_router(todos.router)
    app.include_router(pages.router)
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")
    return app


app = create_app()

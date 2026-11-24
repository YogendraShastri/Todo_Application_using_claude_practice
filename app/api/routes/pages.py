from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.core.config import get_settings

router = APIRouter(include_in_schema=False)


@router.get("/")
def index() -> FileResponse:
    return FileResponse(get_settings().pages_dir / "index.html")

from app.core.config import Settings
from app.repositories.base import TodoRepository
from app.repositories.json_repository import JsonTodoRepository


def build_repository(settings: Settings) -> TodoRepository:
    if settings.storage_backend == "json":
        return JsonTodoRepository(settings.data_file)
    # Future: if settings.storage_backend == "sqlite":
    #     return SqliteTodoRepository(settings.sqlite_url)
    raise ValueError(f"Unknown STORAGE_BACKEND: {settings.storage_backend!r}")

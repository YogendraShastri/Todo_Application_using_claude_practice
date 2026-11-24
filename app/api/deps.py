from functools import lru_cache

from app.core.config import get_settings
from app.repositories.factory import build_repository
from app.services.todo_service import TodoService


@lru_cache
def get_todo_service() -> TodoService:
    return TodoService(build_repository(get_settings()))

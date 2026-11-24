"""Business rules; independent of HTTP and of the storage backend."""
from uuid import uuid4

from app.repositories.base import TodoRepository
from app.schemas.todo import Todo


class EmptyTitleError(ValueError):
    pass


class TodoNotFoundError(LookupError):
    pass


class TodoService:
    def __init__(self, repo: TodoRepository):
        self._repo = repo

    def list_todos(self) -> list[Todo]:
        return self._repo.list()

    def create_todo(self, title: str) -> Todo:
        title = title.strip()
        if not title:
            raise EmptyTitleError("Title cannot be empty")
        return self._repo.add(Todo(id=str(uuid4()), title=title))

    def toggle_todo(self, todo_id: str) -> Todo:
        todo = self._repo.toggle(todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        return todo

    def delete_todo(self, todo_id: str) -> None:
        if not self._repo.delete(todo_id):
            raise TodoNotFoundError(todo_id)

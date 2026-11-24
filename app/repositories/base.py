"""Storage contract. Implement this to add a new backend (e.g. SQLite)."""
from abc import ABC, abstractmethod

from app.schemas.todo import Todo


class TodoRepository(ABC):
    @abstractmethod
    def list(self) -> list[Todo]: ...

    @abstractmethod
    def add(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def toggle(self, todo_id: str) -> Todo | None:
        """Flip `done`; return the updated todo, or None if not found."""

    @abstractmethod
    def delete(self, todo_id: str) -> bool:
        """Return True if a todo was deleted."""

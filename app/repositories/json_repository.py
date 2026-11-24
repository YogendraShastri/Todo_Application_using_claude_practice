import json
import os
from pathlib import Path

from app.repositories.base import TodoRepository
from app.schemas.todo import Todo


class JsonTodoRepository(TodoRepository):
    """Whole-file JSON store. Single-user; no locking. Writes are atomic."""

    def __init__(self, path: Path):
        self._path = path

    def _load(self) -> list[Todo]:
        if not self._path.exists():
            return []
        with self._path.open() as f:
            return [Todo(**item) for item in json.load(f)]

    def _save(self, todos: list[Todo]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self._path.with_suffix(".tmp")
        with tmp.open("w") as f:
            json.dump([t.model_dump() for t in todos], f, indent=2)
        os.replace(tmp, self._path)

    def list(self) -> list[Todo]:
        return self._load()

    def add(self, todo: Todo) -> Todo:
        todos = self._load()
        todos.append(todo)
        self._save(todos)
        return todo

    def toggle(self, todo_id: str) -> Todo | None:
        todos = self._load()
        for todo in todos:
            if todo.id == todo_id:
                todo.done = not todo.done
                self._save(todos)
                return todo
        return None

    def delete(self, todo_id: str) -> bool:
        todos = self._load()
        remaining = [t for t in todos if t.id != todo_id]
        if len(remaining) == len(todos):
            return False
        self._save(remaining)
        return True

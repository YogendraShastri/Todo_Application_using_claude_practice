import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_todo_service
from app.main import app
from app.repositories.json_repository import JsonTodoRepository
from app.services.todo_service import TodoService


@pytest.fixture
def client(tmp_path):
    service = TodoService(JsonTodoRepository(tmp_path / "todos.json"))
    app.dependency_overrides[get_todo_service] = lambda: service
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_crud_flow(client):
    assert client.get("/api/todos").json() == []
    todo = client.post("/api/todos", json={"title": "  a  "}).json()
    assert todo["title"] == "a" and todo["done"] is False
    assert client.patch(f"/api/todos/{todo['id']}").json()["done"] is True
    assert client.delete(f"/api/todos/{todo['id']}").json() == {"ok": True}
    assert client.get("/api/todos").json() == []


def test_errors(client):
    assert client.post("/api/todos", json={"title": "  "}).status_code == 400
    assert client.patch("/api/todos/nope").status_code == 404
    assert client.delete("/api/todos/nope").status_code == 404


def test_pages(client):
    assert client.get("/").status_code == 200
    assert client.get("/static/css/style.css").status_code == 200
    assert client.get("/static/js/main.js").status_code == 200

import json
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "todos.json"
STATIC_DIR = BASE_DIR / "static"

app = FastAPI()


class TodoIn(BaseModel):
    title: str


class Todo(BaseModel):
    id: str
    title: str
    done: bool = False


def load_todos() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open() as f:
        return json.load(f)


def save_todos(todos: list[dict]) -> None:
    with DATA_FILE.open("w") as f:
        json.dump(todos, f, indent=2)


@app.get("/api/todos")
def list_todos() -> list[dict]:
    return load_todos()


@app.post("/api/todos")
def create_todo(payload: TodoIn) -> dict:
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    todos = load_todos()
    todo = {"id": str(uuid4()), "title": title, "done": False}
    todos.append(todo)
    save_todos(todos)
    return todo


@app.patch("/api/todos/{todo_id}")
def toggle_todo(todo_id: str) -> dict:
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            save_todos(todos)
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/api/todos/{todo_id}")
def delete_todo(todo_id: str) -> dict:
    todos = load_todos()
    new_todos = [t for t in todos if t["id"] != todo_id]
    if len(new_todos) == len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    save_todos(new_todos)
    return {"ok": True}


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

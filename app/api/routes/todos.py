from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_todo_service
from app.schemas.todo import Todo, TodoCreate
from app.services.todo_service import (
    EmptyTitleError,
    TodoNotFoundError,
    TodoService,
)

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=list[Todo])
def list_todos(service: TodoService = Depends(get_todo_service)):
    return service.list_todos()


@router.post("", response_model=Todo)
def create_todo(payload: TodoCreate, service: TodoService = Depends(get_todo_service)):
    try:
        return service.create_todo(payload.title)
    except EmptyTitleError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{todo_id}", response_model=Todo)
def toggle_todo(todo_id: str, service: TodoService = Depends(get_todo_service)):
    try:
        return service.toggle_todo(todo_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="Todo not found")


@router.delete("/{todo_id}")
def delete_todo(todo_id: str, service: TodoService = Depends(get_todo_service)):
    try:
        service.delete_todo(todo_id)
    except TodoNotFoundError:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"ok": True}

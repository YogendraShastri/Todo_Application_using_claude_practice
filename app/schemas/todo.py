from pydantic import BaseModel


class TodoCreate(BaseModel):
    title: str


class Todo(BaseModel):
    id: str
    title: str
    done: bool = False

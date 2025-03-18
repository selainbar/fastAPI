from pydantic import BaseModel


class Task(BaseModel):
    title: str
    description: str
    completed: bool
    id: int

def __init__(self, title: str, description: str, id: int, completed: bool = False):
    self.title = title
    self.description = description
    self.completed = completed
    self.id = id
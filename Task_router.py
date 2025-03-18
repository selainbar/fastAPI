from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from Task_model import Task
from JWT_router import verify_token  # Import the verify_token function from your JWT module

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
    responses={404: {"description": "Not found"}},
)



Tasks: dict[str: Task] = {
    "1": {
        "title": "Task 1",
        "description": "This is task 1",
        "completed": False,
        "id": 1
    },
    "2": {
        "title": "Task 2",
        "description": "This is task 2",
        "completed": False,
        "id": 2
    },
    "3": {
        "title": "Task 3",
        "description": "This is task 3",
        "completed": False,
        "id": 3
    }
}

@router.get("/", dependencies = [Depends(verify_token)])
async def getTasks():
    """
    Returns all tasks.
    """
    return Tasks

@router.get("/{task_id}", dependencies = [Depends(verify_token)])
async def getTask(task_id: str):
    """
    Returns a task with the given ID.
    """
    if task_id not in Tasks:
        return JSONResponse(status_code = 404, content = {"message": "Task not found"})
    return Tasks[task_id]

@router.get("/{task_id}/complete", dependencies=[Depends(verify_token)])
async def completeTask(task_id: str):
    """
    Marks a task as completed.
    """
    if task_id not in Tasks:
        return JSONResponse(status_code = 404, content = {"message": "Task not found"})
    Tasks[task_id].completed = True
    return Tasks[task_id]

@router.post("/", dependencies=[Depends(verify_token)])
async def createTask(title: str, description: str):
    """
    Creates a new task with the given title and description.
    """
    if not Tasks:
        new_id = 0
    else:
        max_id = max(int(task_id) for task_id in Tasks.keys())
        new_id = max_id + 1
    task = Task(title = title, description=description, id = new_id, completed = False)  
    Tasks[str(new_id)] = task
    return task

@router.put("/{task_id}", dependencies = [Depends(verify_token)])
async def updateTask(task_id: str, title: str = None, description: str = None):
    """
    Updates a task with the given ID.
    """
    if task_id not in Tasks:
        return JSONResponse(status_code = 404, content = {"message": "Task not found"})
    if title is None and description is None:
        return JSONResponse(status_code = 400, content = {"message": "No fields to update"})
    if title is not None:
        Tasks[task_id]["title"] = title
    if description is not None:
        Tasks[task_id]["description"] = description
    return Tasks[task_id]  

@router.delete("/complete", dependencies=[Depends(verify_token)])
async def deleteCompletedTasks():
    """
    Deletes all tasks that are marked as completed.
    """
    for task_id in list(Tasks.keys()):
        if Tasks[task_id].completed:
            Tasks.pop(task_id)
    return Response(status_code = 204)

@router.delete("/all", dependencies=[Depends(verify_token)])
def deleteAllTasks():
    Tasks.clear()
    return Response(status_code = 204)

@router.delete("/{task_id}", dependencies=[Depends(verify_token)])
async def deleteTask(task_id: str):
    """
    Deletes a task with the given ID.
    """
    if task_id not in Tasks:
        return JSONResponse(status_code = 404, content = {"message": "Task not found"})
    Tasks.pop(task_id)
    return Response(status_code = 204)
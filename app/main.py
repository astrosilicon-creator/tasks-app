from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Tasks API")

# ---- Fake DB in memory for Phase 1 ----
TASKS: list[dict] = []
NEXT_ID = 1

class TaskIn(BaseModel):
    title: str = Field(min_length=1)
    status: str = Field(default="todo", pattern="^(todo|doing|done)$")

class Task(TaskIn):
    id: int

@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: TaskIn):
    global NEXT_ID
    new = {"id": NEXT_ID, **task.model_dump()}
    TASKS.append(new)
    NEXT_ID += 1
    return new

@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return TASKS

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    for t in TASKS:
        if t["id"] == task_id:
            return t
    raise HTTPException(status_code=404, detail="Not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: TaskIn):
    for t in TASKS:
        if t["id"] == task_id:
            t.update(data.model_dump())
            return t
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, t in enumerate(TASKS):
        if t["id"] == task_id:
            TASKS.pop(i)
            return
    raise HTTPException(status_code=404, detail="Not found")

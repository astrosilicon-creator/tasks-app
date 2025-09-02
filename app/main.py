import os

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select

# --- Database ---
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session


class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=120)
    status: str = Field(default="todo", regex="^(todo|doing|done)$")


# --- App ---
app = FastAPI(title="Tasks API")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/ping")
def ping():
    return {"ok": True}


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task, session: Session = Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks(session: Session = Depends(get_session)):
    return session.exec(select(Task)).all()


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: Task, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    task.title = data.title
    task.status = data.status
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(404, "Not found")
    session.delete(task)
    session.commit()
    return

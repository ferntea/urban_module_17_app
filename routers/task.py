# routers/task.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from backend.db_depends import get_db
from models import Task, User
from schemas import CreateTask, UpdateTask  # Assuming you have these schemas defined

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/")
async def all_tasks(db: Session = Depends(get_db)):
    tasks = db.execute(select(Task)).scalars().all()
    return {"tasks": tasks}


@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is not None:
        return task
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


@router.post("/create")
async def create_task(task: CreateTask, user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User  was not found")

    new_task = Task(**task.dict(), user_id=user_id)
    db.add(new_task)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.put("/update/{task_id}")
async def update_task(task_id: int, task: UpdateTask, db: Session = Depends(get_db)):
    db_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if db_task:
        db.execute(update(Task).where(Task.id == task_id).values(**task.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")


@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if db_task:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="Task was not found")

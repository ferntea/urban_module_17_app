# routers/user.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from backend.db_depends import get_db
from models import User, Task
from schemas import CreateUser , UpdateUser   # Assuming you have these schemas defined

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")  # Возвращаем список всех пользователей из БД
async def all_users(db: Session = Depends(get_db)):
    result = db.execute(select(User)).scalars().all()
    return result

@router.get("/{user_id}")  # Извлечение пользователя по user_id
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User  was not found")

@router.get("/{user_id}/tasks")  # Получение всех задач конкретного пользователя
async def tasks_by_user_id(user_id: int, db: Session = Depends(get_db)):
    tasks = db.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    return {"tasks": tasks}

@router.post("/create")  # Добавление нового пользователя в БД
async def create_user(user: CreateUser , db: Session = Depends(get_db)):
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update/{user_id}")  # Обновление пользователя по user_id
async def update_user(user_id: int, user: UpdateUser , db: Session = Depends(get_db)):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user:
        db.execute(update(User).where(User.id == user_id).values(**user.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User  update is successful!"}
    else:
        raise HTTPException(status_code=404, detail="User  was not found")

@router.delete("/delete/{user_id}")  # Удаление пользователя по user_id
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user:
        # Удаление всех задач, связанных с пользователем
        db.execute(delete(Task).where(Task.user_id == user_id))
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User  and associated tasks deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User  was not found")

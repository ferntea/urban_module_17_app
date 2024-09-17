# routers/user.py

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update, delete
from slugify import slugify
from backend.db_depends import get_db
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser


router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")    # Возвращаем список всех пользователей из БД
async def all_users(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User)).scalars().all()
    return result

@router.get("/{user_id}")   # Извлечение пользователя по user_id
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail="User was not found")

@router.post("/create")   # Добавление нового пользователя в БД
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    new_user = User(**user.dict())
    # db.execute(insert(User).values(new_user))
    db.add(new_user)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update/{user_id}")  # Обновление пользователя по user_id
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user:
        db.execute(update(User).where(User.id == user_id).values(**user.dict()))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
    else:
        raise HTTPException(status_code=404, detail="User was not found")

@router.delete("/delete/{user_id}")     # Удаление пользователя по user_id
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    db_user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if db_user:
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {"status_code": status.HTTP_200_OK, "transaction": "User deleted successfully!"}
    else:
        raise HTTPException(status_code=404, detail="User was not found")


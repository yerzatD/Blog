from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..database import get_db
from ..models.User import User
from ..schemas.user_schemas import Token, UserCreate, UserResponse, UserUpdate
from ..services.user_service import UserService

# Prefix in plural to match OAuth2PasswordBearer(tokenUrl="/api/users/token") in auth.py
router = APIRouter(prefix="/api/users", tags=["User"])


@router.post("/register", response_model=UserResponse)
async def register_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await UserService(db).register_user(data)


@router.post("/token", response_model=Token)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    return await UserService(db).login_user(form_data)


@router.get("/info", response_model=UserResponse)
async def get_info(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_info_about_me(current_user)


@router.patch("/update", response_model=UserResponse)
async def update_user(
    data: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    return await UserService(db).update_user(data, current_user)


@router.get("/all", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    return await UserService(db).get_all_users()
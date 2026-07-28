from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..database import get_db
from ..models.User import User
from ..schemas.post_schemas import PostCreate, PostResponse, PostUpdate
from ..services.post_service import PostService

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
async def create_post(
    post_create: PostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await PostService(db).create_post(current_user, post_create)


@router.patch("/update/{post_id}", response_model=PostResponse)
async def update_post(
    data: PostUpdate,
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await PostService(db).update_post(current_user, post_id, data)


@router.get("/post/{post_id}", response_model=PostResponse)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    return await PostService(db).get_post(post_id)


@router.get("/posts", response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    return await PostService(db).get_posts()


@router.get("/user/posts", response_model=List[PostResponse])
async def get_my_posts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await PostService(db).get_user_posts(current_user)


@router.delete("/delete/{post_id}")
async def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await PostService(db).delete_post(current_user, post_id)
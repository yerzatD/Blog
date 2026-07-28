from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.User import User
from ..repositories.post_repository import PostRepository
from ..schemas.post_schemas import PostCreate,PostDelete,PostResponse,PostUpdate
from ..auth import get_current_user
from typing import List
from fastapi import HTTPException,status



class PostService:
    def __init__(self,db:AsyncSession):
        self.db = db
        self.post_repository = PostRepository(db)

    async def create_post(self,current_user : User, data : PostCreate) -> PostResponse:
        post = await self.post_repository.create_post(current_user.id, data)
        return PostResponse.model_validate(post)


    async def update_post(self,current_user : User,post_id: int, data : PostUpdate) -> PostResponse:
        updated_post = await self.post_repository.update_post(current_user.id, post_id, data)
        if updated_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return PostResponse.model_validate(updated_post)

    async def delete_post(self,current_user : User, post_id : int):
        deleted = await self.post_repository.delete_post(current_user.id,post_id)
        if deleted:
            return {"messege" : "Post succsessfully deleted"}
        return {"messege" : "Post not found or process has stopped"}

    async def get_post(self,post_id : int) -> PostResponse:
        post = await self.post_repository.get_post_by_id(post_id)
        if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return PostResponse.model_validate(post)
    
    async def get_user_posts(self,current_user : User) -> List[PostResponse]:
        posts = await self.post_repository.get_user_all_posts(current_user.id)
        return [PostResponse.model_validate(p) for p in posts]


    async def get_posts(self):
        posts = await self.post_repository.get_all_posts()
        return [PostResponse.model_validate(p) for p in posts]
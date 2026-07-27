from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.User import User
from ..repositories.user_repository import UserRepository
from ..schemas.user_schemas import UserCreate, UserUpdate, UserResponse, UserDelete
from fastapi import HTTPException, status


class UserService:
    def __init__(self, db: AsyncSession):
       self.db = db
       self.user_repository = UserRepository(db)
        
    async def create_user(self, user_create: UserCreate) -> UserResponse:
        result = await self.db.execute(select(User).filter(User.email == user_create.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user = await self.user_repository.create_user(user_create)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        user = await self.user_repository.update_user(user_id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.user_repository.get_all_users()
        return [UserResponse.model_validate(user) for user in users]
    async def get_user_by_id(self, user_id: int) -> UserResponse:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserResponse.model_validate(user)

    
    
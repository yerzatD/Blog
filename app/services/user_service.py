from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import create_access_token, verify_password
from ..models.User import User
from ..repositories.user_repository import UserRepository
from ..schemas.user_schemas import Token, UserCreate, UserResponse, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_repository = UserRepository(db)

    async def register_user(self, user_create: UserCreate) -> UserResponse:
        existing_user = await self.user_repository.get_user_by_username(user_create.username)
        if existing_user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        user = await self.user_repository.create_user(user_create)
        return UserResponse.model_validate(user)

    async def login_user(self, form_data: OAuth2PasswordRequestForm) -> Token:
        user = await self.user_repository.get_user_by_username(form_data.username)
        if user is None or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token = create_access_token(data={"sub": str(user.id)})
        return Token(access_token=access_token, token_type="bearer")

    async def update_user(self, user_update: UserUpdate, current_user: User) -> UserResponse:
        user = await self.user_repository.update_user(current_user.id, user_update)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.user_repository.get_all_users()
        return [UserResponse.model_validate(user) for user in users]

    async def get_info_about_me(self, current_user: User) -> UserResponse:
        user = await self.user_repository.get_user_by_id(current_user.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return UserResponse.model_validate(user)
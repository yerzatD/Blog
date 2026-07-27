from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models.User import User
from ..schemas.user_schemas import UserCreate, UserUpdate
from ..auth import hash_password

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_create: UserCreate) -> User:
        new_user = User(
            username=user_create.username,
            about_me=user_create.about_me,
            email=user_create.email,
            hashed_password=hash_password(user_create.password),
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def update_user(self, user_id: int, user_update: UserUpdate) -> User | None:
        user = await self.db.get(User, user_id)
        if user is None:
            return None

        if user_update.username is not None:
            user.username = user_update.username
        if user_update.about_me is not None:
            user.about_me = user_update.about_me
        if user_update.avatar is not None:
            user.avatar = user_update.avatar
        if user_update.password is not None:
            user.hashed_password = hash_password(user_update.password)

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    

    async def get_all_users(self) -> list[User]:
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def get_user_by_id(self, user_id: int) -> User | None:
        user = await self.db.execute(select(User).filter(User.id == user_id))
        return user.scalar_one_or_none()
    
    


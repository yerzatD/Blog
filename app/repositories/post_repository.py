from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.Post import Post
from ..schemas.post_schemas import PostCreate, PostUpdate

class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(self, user_id: int, post_create: PostCreate) -> Post:
        new_post = Post(
            title=post_create.title,
            content=post_create.content,
            post_image=post_create.post_image or "default_post_image.png",
            owner_id=user_id,
        )
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post

    async def update_post(self, post_id: int, post_update: PostUpdate) -> Post | None:
        post = await self.db.get(Post, post_id)
        if post is None:
            return None

        if post_update.title is not None:
            post.title = post_update.title
        if post_update.content is not None:
            post.content = post_update.content
        if post_update.post_image is not None:
            post.post_image = post_update.post_image

        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)
        return post

    async def get_post_by_id(self, post_id: int) -> Post | None:
        post = await self.db.get(Post, post_id)
        return post

    async def get_all_posts(self) -> list[Post]:
        posts = await self.db.execute(select(Post))
        return posts.scalars().all()

    async def delete_post(self, post_id: int) -> bool:
        post = await self.db.get(Post, post_id)
        if post is None:
            return False

        await self.db.delete(post)
        await self.db.commit()
        return True
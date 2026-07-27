from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth import get_current_user
from ..database import get_db
from ..repositories.post_repository import PostRepository
from ..schemas.post_schemas import PostCreate, PostResponse

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
async def create_post(
    post_create: PostCreate,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PostRepository(db)
    post = await repo.create_post(current_user.id, post_create)
    return post

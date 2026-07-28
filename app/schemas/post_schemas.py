from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=10)
    post_image: Optional[str] = Field(None, max_length=200)


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=10)
    post_image: Optional[str] = Field(None, max_length=200)


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    post_image: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PostDelete(BaseModel):
    id: int
    owner_id: int
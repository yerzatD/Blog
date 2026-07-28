from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .post_schemas import PostResponse


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    about_me: Optional[str] = Field(None, max_length=500)
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    about_me: Optional[str] = Field(None, max_length=500)
    avatar: Optional[str] = Field(None, max_length=200)
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    about_me: Optional[str] = None
    email: EmailStr
    avatar: Optional[str] = None
    created_at: datetime
    posts: List[PostResponse]

    model_config = ConfigDict(from_attributes=True)


class UserDelete(BaseModel):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
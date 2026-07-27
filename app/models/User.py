from datetime import datetime

from ..database import Base
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    about_me = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)
    avatar = Column(String, nullable=False, default="default_avatar.png")
    posts = relationship("Post", back_populates="owner", lazy="selectin")
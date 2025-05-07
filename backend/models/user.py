from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.core.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    messages = relationship("Message", back_populates="user")
    chats = relationship("Chat",
                         secondary="user_chat",
                         back_populates="users")
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=320), unique=True, index=True)
    username = Column(String(length=100), unique=True, index=True)
    hashed_password = Column(String(length=1024))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(),
                        server_default=func.now())

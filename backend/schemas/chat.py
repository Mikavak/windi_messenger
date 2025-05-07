from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.models.chat import ChatType


class ChatBase(BaseModel):

    class Config:
        from_attributes = True
        extra = 'ignore'


class ChatCreate(ChatBase):
    """Схема для создания чата"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type_chat: ChatType


class ChatResponseCreate(ChatCreate):
    """Схема ответа после создания чата"""
    id: int
    created_at: datetime = Field(default_factory=datetime.now)


class ChatRead(ChatCreate):
    created_date: datetime
    updated_date: datetime


class ChatUpdate(ChatBase):
    name: Optional[str] = None
    type_chat: Optional[ChatType]


class MessageBase(BaseModel):

    class Config:
        orm_mode = True
        extra = 'ignore'

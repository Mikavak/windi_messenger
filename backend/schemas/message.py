from datetime import datetime

from pydantic import BaseModel, Field


class MessageBase(BaseModel):

    class Config:
        from_attributes = True
        extra = 'ignore'


class MessageCreate(MessageBase):
    """Схема для создания сообщения"""
    chat_id: int
    user_id: int
    message_text: str
    created_at: datetime = Field(default_factory=datetime.now)


class MessageResponseCreate(MessageBase):
    """Схема ответа после создания сообщения"""

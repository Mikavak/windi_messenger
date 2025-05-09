import enum
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, \
    DateTime, Text, Boolean, Table, Enum
from sqlalchemy.orm import relationship

from backend.core.database import Base


class ChatType(str, enum.Enum):
    PERSONAL = "personal"
    GROUP = "group"


class Chat(Base):
    name = Column(String(20), nullable=False)
    type_chat = Column(Enum(ChatType), nullable=False)
    creator_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    creator = relationship(
        "User",
        # Указываю строковое имя в кавычках
        foreign_keys="[Chat.creator_id]",
        lazy="joined"
    )
    users = relationship("User",
                         secondary="user_chat",
                         back_populates="chats")
    created_date = Column(DateTime, default=datetime.now)
    updated_date = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    messages = relationship("Message", back_populates="chat")


class Message(Base):
    chat_id = Column(Integer, ForeignKey("chat.id"), nullable=False)
    chat = relationship("Chat", back_populates="messages")
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="messages")
    message_text = Column(Text, nullable=False)
    created_date = Column(DateTime, default=datetime.now)
    status_read = Column(Boolean, nullable=False, default=False)


# Промежуточная таблица для связи пользователей и чатов
user_chat = Table(
    'user_chat',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('chat_id', Integer, ForeignKey('chat.id'), primary_key=True)
)

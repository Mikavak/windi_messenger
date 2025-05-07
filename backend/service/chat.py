from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.chat import chat_crud
from backend.models import User
from backend.schemas.chat import ChatCreate


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, chat: ChatCreate, creator_id: int):
        user = await self.session.execute(
            select(User).filter(User.id == creator_id))
        user = user.scalar_one()
        new_chat = await chat_crud.create(
            chat,
            self.session,
            creator=user)
        return new_chat

    async def get_all_chats(self):
        return await chat_crud.get_all(self.session)

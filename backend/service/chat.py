from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.chat import chat_crud
from backend.models import User
from backend.schemas.chat import ChatCreate, ChatRead
from backend.service.validators import check_duplicate_chat


class ChatService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_chat(self, chat: ChatCreate, creator_id: int):
        user = await self.session.execute(
            select(User).filter(User.id == creator_id))
        user = user.scalar_one()
        await check_duplicate_chat(chat, user.id, self.session)
        new_chat = await chat_crud.create(
            chat,
            self.session,
            creator=user)
        return new_chat

    async def get_all_chats(self):
        chats = await chat_crud.get_all(self.session)
        results = []
        for chat in chats:
            chat_detail = ChatRead(
                id=chat.id,
                name=chat.name,
                type_chat=chat.type_chat,
                created_date=chat.created_date,
                updated_date=chat.updated_date,
                creator=chat.creator,
            )
            results.append(chat_detail)

        return results

    async def get_one(self, chat_id: int):
        return await chat_crud.get_one(self.session, chat_id)

    async def remove(self, chat_id: int):
        return await chat_crud.remove(self.session, chat_id)
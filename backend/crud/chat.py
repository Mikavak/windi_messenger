from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Chat, User


class CRUDChat:
    def __init__(self, model):
        self.model = model

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            creator: User
    ):
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db_obj.users.append(creator)
        db_obj.creator_id = creator.id
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_all(
            self,
            session: AsyncSession,
    ):
        chats = await session.execute(select(self.model))
        return chats.scalars().all()


chat_crud = CRUDChat(Chat)

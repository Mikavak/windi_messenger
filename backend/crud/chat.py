from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from backend.models import Chat, User
from backend.schemas.chat import ChatUpdate


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
        query = (
            select(self.model)
            # загружаю пользователей (создателя)
            # для отображения вложенного json ответа
            # смотри поле creator в модели Chat
            .options(joinedload(self.model.creator))
        )
        chats = await session.execute(query)
        return chats.scalars().all()

    async def get_one(
            self,
            session: AsyncSession,
            chat_id: int,
    ):
        query = (
            select(self.model)
            .where(self.model.id == chat_id)
        )
        obj = await session.execute(query)
        return obj.scalar()

    async def remove(
            self,
            session: AsyncSession,
            chat_id: int,
    ):
        obj = await self.get_one(session, chat_id)
        await session.delete(obj)
        await session.commit()
        return obj

    async def update(
            self,
            db_obj,
            chat_update: ChatUpdate,
            session: AsyncSession,
    ):
        # Конвертация объекта базы данных в словарь JSON
        obj_data = jsonable_encoder(db_obj)
        # Получение данных для обновления, исключая неустановленные и None
        # значения
        update_data = chat_update.dict(exclude_unset=True, exclude_none=True)
        # Обновление полей объекта
        for field in obj_data:
            if field in update_data:
                # setattr модифицирует текущий объект НЕ СОЗДАЁТ НОВЫЙ
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


chat_crud = CRUDChat(Chat)

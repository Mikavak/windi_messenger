from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Chat


async def check_duplicate_chat(
        chat,
        user_id,
        session: AsyncSession):
    query = select(Chat).where(
        and_(
            Chat.name == chat.name,
            Chat.creator_id == user_id
        )
    )
    result = await session.execute(query)
    if result.scalar():
        raise HTTPException(
            status_code=400,
            detail='Чат с таким именем уже существует!',
        )


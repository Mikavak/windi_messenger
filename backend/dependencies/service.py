from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.service.chat import ChatService


def get_chat_service(
        session: AsyncSession = Depends(get_db)
):
    return ChatService(session)
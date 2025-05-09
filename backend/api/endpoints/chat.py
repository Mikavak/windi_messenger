from fastapi import APIRouter, Depends
from backend.core.user import current_user
from backend.dependencies.service import get_chat_service
from backend.models import User
from backend.schemas.chat import ChatResponseCreate, ChatCreate, ChatRead
from backend.service.chat import ChatService

router = APIRouter()

@router.post(
    '/',
    response_model=ChatResponseCreate
)
async def create_chat(
        chat: ChatCreate,
        # Получить юзера
        user: User = Depends(current_user),
        # Для разделения ответственности между слоями
        # создал сервисный класс для crud действий с объектом
        session: ChatService = Depends(get_chat_service)):
    return await session.create_chat(
        chat,
        creator_id=user.id
    )


@router.get(
    '/',
    response_model=list[ChatRead]
)
async def get_all_chats(
    session: ChatService = Depends(get_chat_service)
):
    chats = await session.get_all_chats()
    return chats

@router.get(
    '/{chat_id}',
    response_model=ChatRead
)
async def get_chat(
        chat_id: int,
        session: ChatService = Depends(get_chat_service)
):
    return await session.get_one(chat_id)


@router.delete(
    '/{chat_id}',
    response_model=ChatRead
)
async def delete_chat(
        chat_id: int,
        session: ChatService = Depends(get_chat_service)
):
    return await session.remove(chat_id)
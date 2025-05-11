from fastapi import APIRouter, Depends, HTTPException
from backend.core.user import current_user
from backend.dependencies.service import get_chat_service
from backend.models import User
from backend.schemas.chat import ChatResponseCreate, ChatCreate, ChatRead, \
    ChatUpdate
from backend.schemas.user import UserAddInChat
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
    # response_model=list[ChatRead]
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
    chat = await session.get_one(chat_id)

    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat


@router.delete(
    '/{chat_id}',
    response_model=ChatRead
)
async def delete_chat(
        chat_id: int,
        session: ChatService = Depends(get_chat_service)
):
    return await session.remove(chat_id)


@router.patch(
    '/{chat_id}',
    response_model=ChatRead,
)
async def update_chat(
        chat_id: int,
        chat: ChatUpdate,
        session: ChatService = Depends(get_chat_service)
):
    return await session.update_chat(chat_id, chat)

@router.patch(
    '/{chat_id}/users',
    response_model=ChatRead
)
async def add_user_in_chat(
        chat_id: int,
        user_data: UserAddInChat,
        current_user: User = Depends(current_user),
        session: ChatService = Depends(get_chat_service)
):
    return await session.add_user_in_chat(
        chat_id,
        user_data,
        current_user.id)
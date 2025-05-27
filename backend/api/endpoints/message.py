from fastapi import APIRouter, Depends

from backend.dependencies.service import get_message_service
from backend.schemas.message import MessageResponseCreate, MessageCreate
from backend.service.message import MessageService

router = APIRouter()

@router.post(
    '/',
    response_model=MessageResponseCreate,
)
async def create_message(
        message: MessageCreate,
        session: MessageService = Depends(get_message_service)
):
    await session.create_message(message)
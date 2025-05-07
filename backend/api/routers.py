from fastapi import APIRouter

from backend.api.endpoints import api_router
from .endpoints import chat_router
main_router = APIRouter()

main_router.include_router(api_router)
main_router.include_router(
    chat_router, prefix="/chat", tags=["chat"]
)

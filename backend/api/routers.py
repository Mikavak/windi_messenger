from fastapi import APIRouter

from backend.api.endpoints import api_router

main_router = APIRouter()

main_router.include_router(api_router)

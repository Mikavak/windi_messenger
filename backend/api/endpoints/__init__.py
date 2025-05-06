from fastapi import APIRouter

from backend.api.endpoints import user

api_router = APIRouter()

api_router.include_router(user.router, prefix="/auth", tags=["auth"])
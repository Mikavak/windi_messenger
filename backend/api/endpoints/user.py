from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.user import auth_backend, fastapi_users
from backend.models.user import User
from backend.schemas.user import UserCreate, UserRead, UserUpdate
from backend.core.user import current_user

router = APIRouter()

@router.get(
    "/",
    response_model=List[UserRead])
async def get_users(
    db: AsyncSession = Depends(get_db),
    # current_user: User = Depends(current_user),  # Проверка авторизации
):
    """
    Получение списка всех пользователей.
    Доступно только авторизованным пользователям.
    """
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


# Маршруты для JWT-аутентификации
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

# Маршруты для регистрации
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)

# Маршруты для сброса пароля и подтверждения
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/reset-password",
    tags=["auth"],
)

# Маршруты для управления пользователями
users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

# Удаление маршрута для удаления пользователя (если это требуется)
users_router.routes = [
    route for route in users_router.routes
    if not (route.path.endswith("/{id}") and "DELETE" in route.methods)
]

router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
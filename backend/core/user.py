from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.config import settings
from backend.core.database import get_db
from backend.models.user import User
from backend.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)

# Настройка транспорта для токенов JWT
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Функция для создания JWT-стратегии


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)


# Создание бэкенда аутентификации
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Класс менеджера пользователей


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        # Проверка минимальной длины пароля
        if len(password) < 8:
            raise InvalidPasswordException(
                reason="Пароль должен содержать минимум 8 символов"
            )
        # Проверка, что пароль не содержит email
        if user.email in password:
            raise InvalidPasswordException(
                reason="Пароль не должен содержать email"
            )

    # Хук, который выполняется после регистрации
    async def on_after_register(
            self, user: User, request: Optional[Request] = None
    ):
        print(f"Пользователь {user.email} зарегистрирован.")

# Зависимость для получения менеджера пользователей


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

# Создание экземпляра FastAPIUsers
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# Зависимости для получения текущего пользователя
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

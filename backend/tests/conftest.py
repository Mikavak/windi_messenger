import pytest
from starlette.testclient import TestClient

from backend.main import app

@pytest.fixture
def client():
    return TestClient(app)








































# import pytest
# from fastapi.testclient import TestClient
# from backend.core.user import current_user
# from backend.main import app
# from unittest.mock import Mock
# from backend.service.chat import ChatService
# from backend.dependencies.service import get_chat_service
# from backend.schemas.chat import ChatResponseCreate
# from datetime import datetime
# from backend.models.user import User
#
#
# @pytest.fixture
# def mock_user():
#     """Создаем тестового пользователя"""
#     return Mock(
#         id=1,
#         email="test@example.com",
#         username="testuser",
#         is_active=True,
#         is_verified=True
#     )
#
#
# class MockChatService:
#     def __init__(self):
#         pass
#
#     async def create_chat(self, chat, creator_id):
#         # Возвращаем объект с правильной структурой для ChatResponseCreate
#         from types import SimpleNamespace
#
#         user_mock = SimpleNamespace(
#             id=creator_id,
#             email="test@example.com",
#             username="testuser"
#         )
#
#         chat_mock = SimpleNamespace(
#             id=1,
#             name=chat.name,
#             type_chat=chat.type_chat,
#             created_at=datetime.now(),
#             users=user_mock  # ChatResponseCreate ожидает users: UserRead
#         )
#
#         return chat_mock
#
# @pytest.fixture
# def client():
#     """Простой TestClient без моков"""
#     with TestClient(app) as test_client:
#         yield test_client
#
#
# @pytest.fixture
# def mock_chat_service():
#     return MockChatService()
#
#
# @pytest.fixture
# def client_with_mocks(mock_user, mock_chat_service):
#     """TestClient со всеми замоканными зависимостями"""
#
#     def mock_current_user():
#         return mock_user
#
#     def mock_get_chat_service():
#         return mock_chat_service
#
#     # Подменяем обе зависимости
#     app.dependency_overrides[current_user] = mock_current_user
#     app.dependency_overrides[get_chat_service] = mock_get_chat_service
#
#     with TestClient(app) as test_client:
#         yield test_client
#
#     app.dependency_overrides.clear()

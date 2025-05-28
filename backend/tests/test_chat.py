from datetime import datetime
import pytest
from httpx import AsyncClient, ASGITransport
from starlette.testclient import TestClient

from backend.dependencies.service import get_chat_service
from backend.main import app
from unittest.mock import Mock
from backend.core.user import current_user
from types import SimpleNamespace


def fake_user_and_service():
    def fake_user():
        user = Mock()
        user.id = 1
        user.username = "Mik"
        user.email = "c@c.ru"
        return user

    def fake_service():
        return MockChatService()
    # Подменна зависимости
    app.dependency_overrides[current_user] = fake_user
    app.dependency_overrides[get_chat_service] = fake_service


class MockChatService:
    async def create_chat(self, chat, creator_id):
        user_mock = SimpleNamespace(
            id=creator_id,
            email="test@example.com",
            username="testuser"
        )

        chat_mock = SimpleNamespace(
            id=1,
            name=chat.name,
            type_chat=chat.type_chat,
            created_at=datetime.now(),
            users=user_mock  # ChatResponseCreate ожидает users: UserRead
        )
        return chat_mock

    async def get_one(self, chat_id):
        user_mock = SimpleNamespace(
            id=1,
            email="test@example.com",
            username="testuser"
        )

        chat_mock = SimpleNamespace(
            id=chat_id,
            name=f"Test Chat {chat_id}",
            type_chat="personal",
            creator=user_mock,
            users=[user_mock],
            created_date=datetime.now(),
            updated_date=datetime.now(),
        )

        return chat_mock


@pytest.mark.asyncio
async def test_get_chat_for_id_with_mok():
    fake_user_and_service()
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as ac:
        response = await ac.get('/chat/1')

        assert response.status_code == 200

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_one_chat_without_mok():
    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
    ) as ac:
        response = await ac.get("/chat/1")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_chats_auth_user():

    fake_user_and_service()

    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test") as ac:

        response = await ac.post("/chat/", json={
            "name": "Mik",
            "type_chat": "personal"
        })
        print(response.json())
        assert response.status_code == 201

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_create_chats_not_auth_user():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://test",
    ) as ac:
        response = await ac.post("/chat/", json={
            "name": "Mik",
            "type_chat": "personal"
        })
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_not_full_data():

    fake_user_and_service()

    async with AsyncClient(
            transport=ASGITransport(app),
            base_url="http://test",
    ) as ac:

        response = await ac.post("/chat/", json={
            "name": "Mik",
        })

        assert response.status_code == 422

    app.dependency_overrides.clear()



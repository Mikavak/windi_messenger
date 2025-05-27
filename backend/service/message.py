from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.message import message_crud


class MessageService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_message(self,message):
        new_message = await message_crud.create(
            message,
            self.session
        )
        return new_message

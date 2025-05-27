from backend.models import Message


class MessageCRUD:
    def __init__(self, model):
        self.model = model

    async def create_message(self, message):
        pass



message_crud = MessageCRUD(Message)
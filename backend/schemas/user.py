from fastapi_users import schemas
from pydantic import Field, BaseModel


class UserRead(schemas.BaseUser[int]):
    username: str
    email: str


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., min_length=3, max_length=50)


class UserUpdate(schemas.BaseUserUpdate):
    username: str = Field(None, min_length=3, max_length=50)


class UserAddInChat(BaseModel):
    user_id: int

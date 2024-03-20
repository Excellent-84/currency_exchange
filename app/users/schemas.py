from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel


class User(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]


class UserInDB(User):
    id: int
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

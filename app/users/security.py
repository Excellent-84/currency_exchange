from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_async_session
from app.db.models import Users
from .exceptions import CredentialsException
from .schemas import TokenData, UserInDB

ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(
    username: str | None, db: AsyncSession = Depends(get_async_session)
) -> UserInDB | None:
    query = select(Users).filter(Users.username == username)
    result = await db.execute(query)
    user = result.scalars().first()
    if user:
        return UserInDB(
            id=user.id,
            username=user.username,
            hashed_password=user.hashed_password
        )
    return None


async def authenticate_user(
    username: str, password: str, db: AsyncSession = Depends(get_async_session)
) -> Union[UserInDB, bool]:
    user = await get_user(username, db)
    if user and verify_password(password, user.hashed_password):
        return user
    return False


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_async_session),
) -> UserInDB:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = TokenData(username=username)
    except JWTError:
        raise CredentialsException
    user = await get_user(db=db, username=token_data.username)
    if user is None:
        raise CredentialsException
    return user

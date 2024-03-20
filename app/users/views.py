from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session
from app.db.models import Users
from .exceptions import LoginException, UserExistsException
from .schemas import Token, UserInDB
from .security import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
    get_user
)

auth_router = APIRouter(prefix="/auth", tags=["AUTH"])


@auth_router.post("/register", response_model=UserInDB, status_code=201)
async def register_in_db(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session),
):
    existing_user = await get_user(form_data.username, db)
    if existing_user:
        raise UserExistsException
    hashed_password = get_password_hash(form_data.password)
    new_user = Users(
        username=form_data.username, hashed_password=hashed_password
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@auth_router.post("/login", status_code=201)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_async_session),
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise LoginException
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="Bearer")


@auth_router.get("/me")
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
    return current_user

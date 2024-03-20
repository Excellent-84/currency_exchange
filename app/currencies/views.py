from typing import Dict, Optional

from fastapi import APIRouter, Depends

from app.users.security import get_current_user
from .external_api import (
    convert_currency, list_of_currencies, rate_currency
)
from .schemas import Exchange, Rate

cur_router = APIRouter(
    prefix="/currency",
    tags=["Currency Exchange"],
    dependencies=[Depends(get_current_user)],
)


@cur_router.get("/list")
async def get_currency_list() -> Optional[Dict[str, str]]:
    """Возвращает список доступных валют."""
    return await list_of_currencies()


@cur_router.get("/rate")
async def get_rate(rate: Rate = Depends()) -> Optional[Dict]:
    """Возвращает курс обмена между двумя валютами."""
    return await rate_currency(rate)


@cur_router.get("/exchange")
async def get_exchange(exc: Exchange = Depends()) -> Optional[Dict]:
    """Конвертирует одну валюту в другую на указанную сумму."""
    return await convert_currency(exc)

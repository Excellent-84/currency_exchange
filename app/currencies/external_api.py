from typing import Dict, Optional

from aiohttp import ClientSession

from app.core.config import settings
from .exceptions import AmountException, CurrencyException, RequestException
from .schemas import Exchange, Rate

API_KEY_CURRENCY = settings.API_KEY

URL = "https://api.apilayer.com/exchangerates_data/"

payload: Dict[str, str] = {}
headers = {"apikey": API_KEY_CURRENCY}


async def make_request(url: str, method: str = "GET") -> Optional[Dict]:
    """Выполняет асинхронный GET-запрос к указанному URL."""
    try:
        async with ClientSession() as session:
            async with session.request(
                method=method, url=url, headers=headers, data=payload
            ) as response:
                return await response.json()
    except Exception:
        raise RequestException


async def list_of_currencies() -> Optional[Dict[str, str]]:
    """Получает список доступных кодов валют."""
    url = URL + "symbols"
    response = await make_request(url)
    return response["symbols"]


async def check_currencies(cur_1: str, cur_2: str) -> bool:
    """Проверяет, что оба кода валют находятся в списке доступных валют."""
    cur_lst = await list_of_currencies()
    if cur_1.upper() not in cur_lst or cur_2.upper() not in cur_lst:
        raise CurrencyException


async def rate_currency(rate: Rate) -> Optional[Dict]:
    """Получает текущий курс обмена между двумя валютами."""
    await check_currencies(rate.cur_1, rate.cur_2)
    url = URL + f"latest?symbols={rate.cur_1}&base={rate.cur_2}"
    return await make_request(url)


async def convert_currency(exc: Exchange) -> Optional[Dict]:
    """Конвертирует одну валюту в другую на указанную сумму."""
    await check_currencies(exc.cur_1, exc.cur_2)
    if exc.amount <= 0:
        raise AmountException
    url = URL + f"convert?to={exc.cur_1}&from={exc.cur_2}&amount={exc.amount}"
    return await make_request(url)

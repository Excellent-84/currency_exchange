from httpx import AsyncClient

from .test_auth_user_veiws import test_login_for_access_token


async def test_get_currency_list(ac: AsyncClient):
    access_token = await test_login_for_access_token(ac)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.get("/currency/list", headers=headers)

    assert response.status_code == 200


async def test_get_rate(ac: AsyncClient):
    access_token = await test_login_for_access_token(ac)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "cur_1": "RUB",
        "cur_2": "btc"
    }
    response = await ac.get("/currency/rate", headers=headers, params=data)

    assert response.status_code == 200
    assert response.json()["success"] is True


async def test_get_exchange(ac: AsyncClient):
    access_token = await test_login_for_access_token(ac)
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "cur_1": "RUB",
        "cur_2": "USD",
        "amount": 2
    }
    response = await ac.get("/currency/exchange", headers=headers, params=data)

    assert response.status_code == 200
    assert response.json()["success"] is True

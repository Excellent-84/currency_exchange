from httpx import AsyncClient


async def test_register_in_db(ac: AsyncClient):
    response = await ac.post("/auth/register", data={
        "username": "test_user",
        "password": "test_password"
    })

    assert response.status_code == 201


async def test_login_for_access_token(ac: AsyncClient):
    response = await ac.post("/auth/login", data={
        "username": "test_user",
        "password": "test_password"
    })

    assert response.status_code == 201
    assert response.json()["token_type"] == "Bearer"

    return response.json()["access_token"]


async def test_read_users_me(ac: AsyncClient):
    access_token = await test_login_for_access_token(ac)
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await ac.get("/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == "test_user"

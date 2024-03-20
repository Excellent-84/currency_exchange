## Проект «API обмена валют»

### Описание проекта:

Асинхронный програмный интерфейс, по средствам которого пользователи могут
получать последние курсы обмена различных валют и выполнять их конвертацию.
Проект включает аутентификацию с помощью JWT-токена для доступа пользователей
и интеграцию с открытым API для получения данных об обменных курсах в режиме
реального времени.

### Стек технологий:
<img src="https://img.shields.io/badge/Python-FFFFFF?style=for-the-badge&logo=python&logoColor=3776AB"/><img src="https://img.shields.io/badge/FastAPI-FFFFFF?style=for-the-badge&logo=fastapi&logoColor=009688"/><img src="https://img.shields.io/badge/pydantic-FFFFFF?style=for-the-badge&logo=pydantic&logoColor=E92063"/><img src="https://img.shields.io/badge/aiohttp-FFFFFF?style=for-the-badge&logo=aiohttp&logoColor=2C5BB4"/><img src="https://img.shields.io/badge/PostgreSQL-FFFFFF?style=for-the-badge&logo=PostgreSQL&logoColor=4169E1"/><img src="https://img.shields.io/badge/sqlalchemy-FFFFFF?style=for-the-badge&logo=sqlalchemy&logoColor=D71F00"/><img src="https://img.shields.io/badge/alembic-FFFFFF?style=for-the-badge&logo=alembic&logoColor=8212"/><img src="https://img.shields.io/badge/JWT-FFFFFF?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=black"/><img src="https://img.shields.io/badge/pytest-FFFFFF?style=for-the-badge&logo=pytest&logoColor=0A9EDC"/>

### Как запустить проект:

##### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Excellent-84/currency_exchange.git
cd currency_exchange
```

##### Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
```

##### Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

##### Создать файл .env и указать необходимые токены по примеру .env.example:
```
touch .env
```

##### При необходимости выполнить и применить миграции:

```
alembic revision --autogenerate -m "<ваш комментарий>"
alembic upgrade head
```

##### Запустить проект:

```
python main.py
```

##### Тестирование. Перед запуском тестирования в файле .test.env
##### необходимо указать тестовые данные, отличные от файла .env:

```
pytest
```

### Примеры запросов к API с помощью Postman:

##### Регистрация пользователя в базе данных:

Во вкладке Body выбрать x-www-form-urlencoded.
В поле key указать username и password.
В поле value указать их значение.

Метод POST к эндпоинту   http://127.0.0.1:8000/auth/register

Пример ответа:

```
{
    "username": "John Doe",
    "id": 15,
    "hashed_password": "$2b$12$BUQluFx5OoTnH34TKuS1OuOPDrTj7DcdnjZrBhdm83Y/PtOe5TYJ."
}
```

##### Аутентификация пользователя:

Оставить те же поля и их значения, которые указывали при регистрации.
Срок действия токена 30 минут, после чего необходимо пройти повторную аутентификацию


Метод POST к эндпоинту   http://127.0.0.1:8000/auth/login

Пример ответа:

```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJKYW5lIEFpciIsImV4cCI6MTcxMDk0MTkwOH0.rETSvS9FU5qpOmp6QURw_TLxNnYa7JDBSEaOGC2EdUk",
    "token_type": "Bearer"
}
```

##### Получение списка доступных валют:

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.

Метод GET к эндпоинту   http://127.0.0.1:8000/currency/list

Пример ответа:

```
{
    "AED": "United Arab Emirates Dirham",
    "AFN": "Afghan Afghani",
    "ALL": "Albanian Lek",
    ...
}
```

##### Получение курса пары доступных валют:

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.
Во вкладке Params в поле key указать cur_1 и cur_2.
В поле value указать их значение по ключу из списка доступных валют.
Например пара RUB и USD.

Метод GET к эндпоинту   http://127.0.0.1:8000/currency/rate

Пример ответа:

```
{
    "success": true,
    "timestamp": 1710943326,
    "base": "USD",
    "date": "2024-03-20",
    "rates": {
        "RUB": 92.249758
    }
}
```

##### Конвертация пары доступных валют:

Во вкладке Auth в поле Type выбрать Bearer Token.
В поле Token скопировать значение access_token, полученного при аутентификации.
Во вкладке Params в поле key указать cur_1, cur_2, а также amount.
В поле value указать их значение по ключу из списка доступных валют.
Значение для ключа amount указать любое положительное число.
Например пара RUB и BTC, колчество 0.5.

Метод GET к эндпоинту   http://127.0.0.1:8000/currency/exchange

Пример ответа:

```
{
    "success": true,
    "query": {
        "from": "BTC",
        "to": "RUB",
        "amount": 0.5
    },
    "info": {
        "timestamp": 1710944165,
        "rate": 5898969.225331
    },
    "date": "2024-03-20",
    "result": 2949484.612666
}
```

##### Подробную версию запросов можно посмотреть по адресу:
##### http://127.0.0.1:8000/docs/ или http://127.0.0.1:8000/redoc/

#### Автор: [Горин Евгений](https://github.com/Excellent-84)

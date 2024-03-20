import uvicorn
from fastapi import FastAPI

from app.currencies.views import cur_router
from app.users.views import auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(cur_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

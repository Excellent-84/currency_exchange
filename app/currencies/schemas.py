from pydantic import BaseModel


class Rate(BaseModel):
    cur_1: str
    cur_2: str


class Exchange(Rate):
    amount: float = 1

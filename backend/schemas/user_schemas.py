from pydantic import BaseModel
from typing import Optional, List

# Схемы для пользователей
class UserBase(BaseModel):
    username: str
    lastname: str
    email: str
    password: str
    position: str
    department: str
    workplace: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
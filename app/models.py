# models.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class ShowUser(BaseModel):
    name: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True

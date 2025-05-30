from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

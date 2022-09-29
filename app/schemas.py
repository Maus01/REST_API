from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserPublic(BaseModel):
    email: EmailStr
    id: int
    created: datetime

    class Config:
        orm_mode=True

class NewUser(BaseModel):
    email: EmailStr
    password: str

class Article(BaseModel):
    title: str
    content: str


class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    created: datetime
    owner_id: int
    owner: UserPublic
    
    class Config:
        orm_mode=True


class TokenData(BaseModel):
    id: int

class Token(BaseModel):
    acces_token: str
    token_type: str

class ChangePassword(BaseModel):
    new_password: str
    old_password: str
    

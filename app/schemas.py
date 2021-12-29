from typing import Optional
from pydantic import BaseModel, EmailStr ,conint
from datetime import datetime

from .models import User

class UserCreate(BaseModel):
    email: EmailStr
    password:str

class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at : datetime
    class Config:           
        orm_mode= True              # tell the Pydantic model to read the data even if it is not a dict (such as SQLAlchemy Model)

class UserLogin(BaseModel):
    email: EmailStr
    password : str

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at : datetime
    owner_id : int
    owner: UserOut
    class Config:
        orm_mode= True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None
    # created_at : datetime


class Vote(BaseModel):
    post_id : int
    # dir: conint(ge=0, le=1)
    voted: bool


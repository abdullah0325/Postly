from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ========== User Schemas ==========

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# ========== Auth Schemas ==========

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


# ========== Post Schemas ==========

class PostCreate(BaseModel):
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None


class PostOut(BaseModel):
    id: int
    title: str
    content: Optional[str]
    image_url: Optional[str]
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config:
        orm_mode = True


# ========== Comment Schemas ==========

class CommentCreate(BaseModel):
    text: str


class CommentOut(BaseModel):
    id: int
    text: str
    created_at: datetime
    user_id: int
    post_id: int
    user: UserOut

    class Config:
        orm_mode = True


# ========== Like Schemas ==========

class LikeOut(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
    user: UserOut

    class Config:
        orm_mode = True


from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

class MessageOut(BaseModel):
    id: int
    content: str
    sender_id: int
    receiver_id: int
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True

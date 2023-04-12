from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class post_template(BaseModel):
    title: str 
    content: str
    published: bool = True
    
class response_template(BaseModel):
    title: str
    user_id: int
    content: str
    published: bool
    
    class Config:
        orm_mode = True


class NewUser(BaseModel):
     email: EmailStr
     password: str
     
class UserOut(BaseModel):
    id: str
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None

class Like(BaseModel):
    post_id: int
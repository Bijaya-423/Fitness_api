from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    trainer = "trainer"
    gym = "gym"
    admin = "admin"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum    # client, trainer, gym_owner, admin

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenRequest(BaseModel):
    refresh_token: str
    

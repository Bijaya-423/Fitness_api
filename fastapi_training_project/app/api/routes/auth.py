from fastapi import APIRouter
from app.models.auth import UserCreate, UserLogin, TokenRequest
from app.controllers.auth import register_user, login_user, refresh_token_user

router = APIRouter()

@router.post("/auth/register")
def register(user: UserCreate):
    return register_user(user)

@router.post("/auth/login")
def login(user: UserLogin):
    return login_user(user)

@router.post("/auth/refresh-token")
def refresh(data: TokenRequest):
    return refresh_token_user(data.refresh_token)


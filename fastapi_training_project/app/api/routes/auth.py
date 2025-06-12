from fastapi import APIRouter, UploadFile, File, Depends, Form
from app.models.auth import UserCreate, UserLogin, TokenRequest
from app.controllers.auth import register_user, login_user, refresh_token_user,  upload_kyc_documents, get_user_profile, update_user_profile
from typing import List
from bson import ObjectId

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


@router.post("/user/kyc-upload")
async def upload_kyc(user_id: str = Form(...), files: List[UploadFile] = File(...)):
    return upload_kyc_documents(user_id, files)

@router.get("/user/profile")
def get_profile(user_id: str):
    return get_user_profile(user_id)

@router.put("/user/profile")
def update_profile(
    user_id: str,
    name: str = Form(None),
    phone: str = Form(None),
    address: str = Form(None)
):
    update_data = {}
    if name: update_data["name"] = name
    if phone: update_data["phone"] = phone
    if address: update_data["address"] = address
    return update_user_profile(user_id, update_data)


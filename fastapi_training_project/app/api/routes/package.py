# app/api/routes/package.py

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_packages():
    return {"message": "Package router is working"}

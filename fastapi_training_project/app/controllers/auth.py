from fastapi import HTTPException, status
from app.config.database import db
from passlib.hash import bcrypt
from jose import jwt
import os
from datetime import datetime, timedelta
from bson import ObjectId  # Add this import

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_REFRESH_SECRET = os.getenv("JWT_REFRESH_SECRET")

users_collection = db["users"]

def generate_tokens(user):
    payload = {"id": str(user["_id"]), "role": user["role"], "exp": datetime.utcnow() + timedelta(hours=1)}
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    refresh_payload = {"id": str(user["_id"]), "role": user["role"], "exp": datetime.utcnow() + timedelta(days=1)}
    refresh_token = jwt.encode(refresh_payload, JWT_REFRESH_SECRET, algorithm="HS256")
    return {"token": token, "refresh_token": refresh_token}

'''# def register_user(user_data):
#     existing = users_collection.find_one({"email": user_data.email})
#     if existing:
#         raise HTTPException(status_code=400, detail="User already exists")

#     hashed_password = bcrypt.hash(user_data.password)
#     user_dict = user_data.dict()
#     user_dict["password"] = hashed_password
#     result = users_collection.insert_one(user_dict)
#     return {"message": "User registered successfully", "user_id": str(result.inserted_id)}'''

def register_user(user_data):
    VALID_ROLES = {"user", "trainer", "gym", "admin"}
    
    if user_data.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role. Must be one of: user, trainer, gym, admin")

    existing = users_collection.find_one({"email": user_data.email})
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = bcrypt.hash(user_data.password)
    user_dict = user_data.dict()
    user_dict["password"] = hashed_password
    result = users_collection.insert_one(user_dict)
    return {"message": "User registered successfully", "user_id": str(result.inserted_id)}



def login_user(user_data):
    user = users_collection.find_one({"email": user_data.email})
    if not user or not bcrypt.verify(user_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return generate_tokens(user)


'''# def refresh_token_user(refresh_token):
#     try:
#         decoded = jwt.decode(refresh_token, JWT_REFRESH_SECRET, algorithms=["HS256"])
#         user = users_collection.find_one({"_id": decoded["id"]})
#         if not user:
#             raise HTTPException(status_code=401, detail="User not found")
#         return generate_tokens(user)
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=403, detail="Refresh token expired")
#     except jwt.JWTError:
#         raise HTTPException(status_code=403, detail="Invalid refresh token")
    '''


def refresh_token_user(refresh_token):
    try:
        decoded = jwt.decode(refresh_token, JWT_REFRESH_SECRET, algorithms=["HS256"])
        user_id = decoded.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = users_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return generate_tokens(user)

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
import os
import time
from datetime import timedelta, datetime
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from starlette.responses import JSONResponse

from app.db.base import customers_collection
from app.models.error import APIResponseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_email(email: str):
    customer = customers_collection.find_one({'email': email, 'is_deleted': False})
    return customer


# crate error response
def get_error_response(message: str, status_code: int):
    response = APIResponseModel(status=False, message=message).dict()
    return JSONResponse(status_code=status_code, content=response)


# generate timestamp in milliseconds
def get_timestamp():
    return time.time_ns() // 1_000_000


def get_hashed_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.environ['SECRET_KEY'], algorithm=os.environ['ALGORITHM'])
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(email, password):
    user: object = get_user_email(email)
    if not user:
        return None
    if not verify_password(password, user.get('password')):
        return None
    return user

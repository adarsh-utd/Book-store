import os
import time
from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from starlette.responses import JSONResponse

from app.db.base import customers_collection
from app.models.customers import CustomerModel, TokenData
from app.models.error import APIResponseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


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


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms=[os.environ["ALGORITHM"]])
        email: str = str(payload.get("sub"))
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user_email(str(token_data.email))
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(
        current_user: CustomerModel = Depends(get_current_user)):
    return current_user

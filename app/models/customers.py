from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field

from app.models.base import PyObjectId


class Customers(BaseModel):
    name: str
    password: str
    email: EmailStr

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password": "password",
            }
        }


class CustomerModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: EmailStr
    password: str
    signed_up_ts: int
    is_deleted: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class LoginResponseModel(BaseModel):
    id: str
    name: str
    email: str
    access_token: str
    access_token_expiry_time: int


class Login(BaseModel):
    email: EmailStr
    password: str

    class config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "jdoe@example.com",
                "password": "password",
            }
        }

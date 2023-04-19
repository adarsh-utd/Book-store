from enum import Enum
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.base import PyObjectId


class BookRequestModel(BaseModel):
    name: str
    description: str
    image: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Books(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    image: Optional[str] = None
    is_deleted: bool = False

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

    def list_books(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "image": self.image
        }


class LikeDislike(str, Enum):
    like = 'like'
    dislike = 'dislike'


class BookUpdateRequestModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
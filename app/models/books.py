from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class BookRequestModel(BaseModel):
    name: str
    description: str
    image: Optional[str] = None

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

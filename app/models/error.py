from typing import Optional

from pydantic import BaseModel


class APIResponseModel(BaseModel):
    status: bool
    message: Optional[str]
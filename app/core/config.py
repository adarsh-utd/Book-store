
from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES :int = 2880




settings = Settings()
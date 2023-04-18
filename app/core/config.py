import redis
from pydantic import BaseSettings


class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 2880
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def redis_instance(self):
        return redis.Redis(host=self.redis_host, port=self.redis_port, db=self.redis_db)


settings = Settings()

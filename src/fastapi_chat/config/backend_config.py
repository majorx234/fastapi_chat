from typing import Set, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from datetime import timedelta


class Config(BaseSettings):
    # webserver
    host: str = '0.0.0.0'
    port: int = 8000
    allowed_origins: Set[str] = set(["http://0.0.0.0:8000"])

    # database
    db_hostname: str = Field(default="db", alias="POSTGRES_HOST")
    db_port: int = 5432
    db_user: str = "testuser"
    db_password: str = "1312"

    # token handler
    secret_key: str = Field(default="1312", alias="TOKEN_KEY")
    token_expire_time: timedelta = timedelta(minutes=30)

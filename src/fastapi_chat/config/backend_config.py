from typing import Set, Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    host: str = '0.0.0.0'
    port: int = 8000
    allowed_origins: Set[str] = set(["http://0.0.0.0:8000"])

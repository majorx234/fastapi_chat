from pydantic import BaseModel
from typing import Optional
from enum import Enum


class UserRole(Enum):
    """Role as Enum"""
    ADMIN = "admin"
    CHATTER = "chatter"
    AI = "ai"
    VIEWER = "viewer"


class User(BaseModel):
    """User-Model"""
    username: str
    email: str
#    first_name: Optional[str] = None
#    last_name: Optional[str] = None
    role: UserRole
    is_active: Optional[bool] = True


class DbUser(BaseModel):
    """user Model  for DataBase"""
    hashed_password: str


class UserCreate(BaseModel):
    """Model to create a User"""
    username: str
# TODO: add properties
#    email: str
#    first_name: str
#    last_name: str
    role: UserRole
    hashed_password: str


class LoginUser(BaseModel):
    username: str
    hashed_password: str

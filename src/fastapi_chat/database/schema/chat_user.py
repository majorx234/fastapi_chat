from sqlmodel import SQLModel, Field


class ChatUser(SQLModel, table=True):
    __tablename__ = 'chatuser'
    username: str = Field(primary_key=True)
    email: str
    role: str
    hashed_password: str

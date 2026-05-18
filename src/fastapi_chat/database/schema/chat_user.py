from sqlmodel import SQLModel, Field


class ChatUser(SQLModel, table=True):
    __tablename__ = 'chatuser'
    id: int = Field(primary_key=True)
    username: str
    email: str
    role: str
    hashed_password: str

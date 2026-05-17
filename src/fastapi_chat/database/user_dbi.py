from sqlmodel import select
from fastapi_chat.database import DatabaseSession
from fastapi_chat.database.schema.chat_user import ChatUser
from sqlalchemy import text


class UserDBI:
    def __init__(self, db: DatabaseSession):
        self.db = db

    def get_user(self):
        sql_statement = select(ChatUser)
        return self.db.query(sql_statement)

import secrets
from sqlmodel import select
from fastapi_chat.database import DatabaseSession
from fastapi_chat.database.schema.chat_user import ChatUser
from sqlalchemy import text
import logging as log


class UserDBI:
    def __init__(self, db: DatabaseSession):
        self.db = db

    def get_user(self):
        sql_statement = select(ChatUser)
        users = []
        for user in self.db.query(sql_statement):
            users.append(user)
        return users

    def login(self, username: str, password: str):
        sql_statement = select(ChatUser).where(ChatUser.username == username)
        db_user = self.db.query(sql_statement).first()
        if db_user:
            checked_password = secrets.compare_digest(password,
                                                      db_user.hashed_password)
            if checked_password:
                return True
            log.error(f"invalid credentials of user '{username}'!")
        return False

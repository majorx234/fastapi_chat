from fastapi import APIRouter, Request, status
import json
from fastapi_chat.database import DatabaseSession
from fastapi_chat.database.user_dbi import UserDBI
from fastapi_chat.models.user import LoginUser


class LoginRouter:
    def __init__(self, db: DatabaseSession):
        self.user_dbi = UserDBI(db)
        self._router = APIRouter(
            prefix="/login",
            tags=['web socket'],
        )
        self._router.add_api_route(
            "/login",
            self.post_user_psw,
            methods=["POST"]
        )
        self._router.add_api_route(
            "/get_user_psw",
            self.get_user_psw,
            methods=["GET"]
        )
        self._router.add_api_route(
            "/post_user_psw",
            self.post_user_psw,
            methods=["POST"]
        )

    def post_user_psw(self, user: LoginUser, request: Request):
        print(f'user: {user}')
        if self.user_dbi.login(user.username, user.hashed_password):
            return status.HTTP_200_OK
        return status.HTTP_401_UNAUTHORIZED

    def get_user_psw(self):
        print("get_user_psw")
        user = self.user_dbi.get_user()
        print(f'login_router get_user_psw() -> user: {user}')
        return status.HTTP_200_OK

    def get_router(self):
        return self._router

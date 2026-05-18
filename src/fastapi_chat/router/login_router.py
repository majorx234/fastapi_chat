from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse
import json
from fastapi_chat.database import DatabaseSession
from fastapi_chat.database.user_dbi import UserDBI
from fastapi_chat.models.user import LoginUser, LoginInfo
from fastapi_chat.token_handler import TokenHandler


class LoginRouter:
    def __init__(self, db: DatabaseSession, token_handler: TokenHandler):
        self.user_dbi = UserDBI(db)
        self.token_handler = token_handler
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
        typeof_username = type(user.username)
        access_token = None
        http_status = status.HTTP_401_UNAUTHORIZED
        msg = "error user/psw invalid"
        if self.user_dbi.login(user.username, user.hashed_password):
            http_status = status.HTTP_200_OK
            access_token = self.token_handler.create_access_token(user.username)
            msg = "login succesful"
        return JSONResponse(
            LoginInfo(
                token=access_token,
                role="chatter",
                info_msg=msg).dict(),
            http_status)

    def get_user_psw(self):
        print("get_user_psw")
        user = self.user_dbi.get_user()
        print(f'login_router get_user_psw() -> user: {user}')
        return status.HTTP_200_OK

    def get_router(self):
        return self._router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastapi_chat.config.backend_config import Config
from fastapi_chat.connection_manager import ConnectionManager
from fastapi_chat.router.ws_router import WsRouter
from fastapi_chat.database import DatabaseSession


class Backend:
    """
    A class to represent the backend.
     ...
     """
    def __init__(self,
                 config: Config,
                 db: DatabaseSession):

        self.db = db
        manager = ConnectionManager()
        self.app = FastAPI(
            title="FastAPI ChatServer",
            description="backend functionalities for chat backend",
            swagger_ui_parameters={"persistAuthorization": True}
        )

        # allowing cors
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # set up routers
        ws_router = WsRouter(manager)
        self.app.include_router(ws_router.get_router())
        self.app.mount("/",
                       StaticFiles(directory="./src/fastapi_chat/static"),
                       name="static")

    def get_app(self):
        return self.app

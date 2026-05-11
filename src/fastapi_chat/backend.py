from fastapi import (
        FastAPI,
        Request,
        status
)
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from fastapi_chat.config.backend_config import Config


class Backend:
    """
    A class to represent the backend.
     ...
     """
    def __init__(self,
                 config: Config):
        self.app = FastAPI(
            title="FastAPI ChatServer",
            description="backend functionalities for chat backend",
            swagger_ui_parameters={"persistAuthorization": True}
        )
        self.app.mount("/",
                       StaticFiles(directory="./src/fastapi_chat/static"), name="static")

        # allowing cors
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def get_app(self):
        return self.app

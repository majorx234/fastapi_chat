#!/usr/bin/env python3

from os import path
import uvicorn

from fastapi_chat.config.backend_config import Config
from fastapi_chat.backend import Backend
from fastapi_chat.database import DatabaseSession


def main():
    """
    Main class which gets called first when program starts
    """
    config = Config()
    db = DatabaseSession(config)
    backend = Backend(config, db)

    uvicorn.run(backend.get_app(),
                host=config.host,
                port=config.port,
                log_config="./src/fastapi_chat/config/log_conf.yaml")


if __name__ == '__main__':
    main()

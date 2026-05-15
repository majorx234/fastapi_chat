from sqlmodel import Session, create_engine, select
from fastapi_chat.config.backend_config import Config


class DatabaseSession:
    def __init__(self, config: Config):
        user = config.db_user
        password = config.db_password
        hostname = config.db_hostname
        port = config.db_port
        db_name = "test_db"

        self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{hostname}:{port}/{db_name}')

        self.session = Session(self.engine)

    def query(self, sql_statement):
        rows = []
        for row in self.session.exec(sql_statement):
            rows.append(row)
        return rows

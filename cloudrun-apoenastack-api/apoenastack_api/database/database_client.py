import os
import pg8000
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# from google.cloud.sql.connector import Connector, IPTypes


class DatabaseClient:
    def __init__(self) -> None:
        if not os.getenv("ENV"):
            raise Exception("Not ENV environment variable available")
        if os.environ["ENV"] == "local":
            self.database = "postgresql://postgres:postgres@localhost:5432/fakedata"
            self.engine = create_engine(
                self.database
            )
            self.session = sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=self.engine)
        elif os.environ["ENV"] == "dev":
            self.database = "postgresql://postgres:postgres@host.docker.internal:5432/fakedata"
            self.engine = create_engine(
                self.database
            )
            self.session = sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=self.engine)
        elif os.environ["ENV"] == "prd":
            self.engine = self.__get_conn()
        else:
            raise Exception(f"Value of ENV variable ({os.environ['ENV']}) invalid")

    def __get_conn(self) -> pg8000.dbapi.Connection:
        print("Chamada de Sessão da Base de Dados")
        project_id = os.getenv("PROJECT_ID", "")
        region = os.getenv("REGION", "southamerica-east1")
        instance = os.getenv("INSTANCE", "apoena-database")
        unix_socket_path = f"/cloudsql/{project_id}:{region}:{instance}"
        db_user = os.getenv("DB_USER", "")
        db_pass = os.getenv("DB_PASS", "")
        db_name = os.getenv("DB_NAME", "")

        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="postgresql+pg8000",
                username=db_user,
                password=db_pass,
                database=db_name,
                query={"unix_sock": f"{unix_socket_path}/.s.PGSQL.5432"},
            )
        )
        return engine

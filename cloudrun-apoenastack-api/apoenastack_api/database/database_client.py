import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud.sql.connector import Connector, IPTypes
import pg8000


class DatabaseClient:
    def __init__(self) -> None:
        if not os.getenv("ENV"):
            raise Exception("Not ENV environment variable available")
        if os.environ["ENV"] == "local":
            self.database = "postgresql://postgres:postgres@localhost:5432/fakedata"
            self.engine = create_engine(
                self.database
            )
        elif os.environ["ENV"] == "dev":
            self.database = "postgresql://postgres:postgres@host.docker.internal:5432/fakedata"
            self.engine = create_engine(
                self.database
            )
        elif os.environ["ENV"] == "prd":
            self.engine = create_engine("postgresql+pg8000://", creator=self.__get_conn)

        else:
            raise Exception(f"Value of ENV variable ({os.environ['ENV']}) invalid")

        self.session = sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=self.engine)

    def __get_conn(self) -> pg8000.dbapi.Connection:
        print("Chamada de Sessão da Base de Dados")
        project_id = os.getenv("PROJECT_ID", "")
        region = os.getenv("REGION", "southamerica-east1")
        instance = os.getenv("INSTANCE", "apoena-database")
        instance_connection_name = f"{project_id}:{region}:{instance}"
        db_user = os.getenv("DB_USER", "")
        db_pass = os.getenv("DB_PASS", "")
        db_name = os.getenv("DB_NAME", "")

        ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

        connector = Connector(ip_type)

        conn = connector.connect(
            instance_connection_name,
            "pg8000",
            user=db_user,
            password=db_pass,
            db=db_name
        )
        return conn

    def __call__(self):
        print("Chamada de Sessão da Base de Dados")
        return self.session()

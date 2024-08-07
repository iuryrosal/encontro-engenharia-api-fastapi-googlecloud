import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseClient:
    def __init__(self) -> None:
        if os.getenv("env", "dev") == "dev":
            self.database = "postgresql://postgres:postgres@localhost:5432/fakedata"

        self.engine = create_engine(
            self.database
        )

        self.session = sessionmaker(autocommit=False,
                                    autoflush=False,
                                    bind=self.engine)

    def __call__(self):
        return self.session()

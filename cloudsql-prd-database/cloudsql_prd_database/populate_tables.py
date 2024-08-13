from sqlalchemy import create_engine, MetaData
from hashlib import sha256
from faker import Faker
import sys
import os
import pg8000
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Column, String, Date, Table
from google.cloud.sql.connector import Connector, IPTypes


class GenerateData:
    """
    generate a specific number of records to a target table in the
    postgres database.
    """

    faker = Faker('pt_BR')

    def __init__(self):
        """
        define command line arguments.
        """
        self.table = sys.argv[1]
        self.num_records = int(sys.argv[2])
        self.metadata = MetaData()

        load_dotenv()

        if os.getenv('ENV', '') == "prd":
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('SA_KEYFILE')
            self.engine = create_engine("postgresql+pg8000://", creator=self.__get_conn)

        with self.engine.connect() as conn:
            self.metadata.reflect(conn)

    def __get_conn(self) -> pg8000.dbapi.Connection:
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

    def create_data(self):
        """
        using the faker library, generate data and execute DML.
        """

        if self.table not in self.metadata.tables.keys():
            return print(f"{self.table} does not exist")

        if self.table == "customers":
            with self.engine.begin() as conn:
                for _ in range(self.num_records):
                    fake_customer_insert_command = self.__insert_fake_customer()
                    conn.execute(fake_customer_insert_command)

    def __insert_fake_customer(self):
        table = self.metadata.tables[self.table]
        insert_command = table.insert().values(
            cd_customer=sha256(self.faker.cpf().encode("utf-8")).hexdigest(),
            nm_customer=self.faker.name(),
            st_email=self.faker.email(),
            st_phone=self.faker.phone_number(),
            sg_state=self.faker.state()[0],
            dt_birth=self.faker.date_of_birth(minimum_age=18,
                                              maximum_age=80)
        )
        return insert_command


if __name__ == "__main__":
    generate_data = GenerateData()
    generate_data.create_data()

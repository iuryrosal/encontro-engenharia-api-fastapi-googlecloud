from sqlalchemy import create_engine, MetaData
from hashlib import sha256
from faker import Faker
import sys


class GenerateData:
    """
    generate a specific number of records to a target table in the
    postgres database.
    """

    faker = Faker('pt_BR')
    metadata = MetaData()
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5432/fakedata"
    )

    def __init__(self):
        """
        define command line arguments.
        """
        self.table = sys.argv[1]
        self.num_records = int(sys.argv[2])

        with self.engine.connect() as conn:
            self.metadata.reflect(conn)

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

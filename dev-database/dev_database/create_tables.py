from sqlalchemy import create_engine, MetaData, Column, String, Date, Table

engine = create_engine(
    "postgresql://postgres:postgres@localhost:5432/fakedata"
)

# Create a metadata object
metadata = MetaData()

customers_table = Table(
    "customers",
    metadata,
    Column("cd_customer", String(256), primary_key=True),
    Column("nm_customer", String(135), nullable=False),
    Column("st_email", String(135), nullable=False),
    Column("st_phone", String(135), nullable=False),
    Column("sg_state", String(2), nullable=False),
    Column("dt_birth", Date, nullable=False)
)

with engine.begin() as conn:
    metadata.create_all(conn)
    for table in metadata.tables.keys():
        print(f"{table} successfully created")

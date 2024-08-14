from fastapi import FastAPI, Request
from http import HTTPStatus
from apoenastack_api.schemas import Message, Customer
from apoenastack_api.database.models import Customers
from apoenastack_api.database.database_client import DatabaseClient
from sqlalchemy import text

app = FastAPI()


@app.get("/health_check", status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {"message": "API Activated!"}


@app.get("/customers/{cd_customer}", status_code=HTTPStatus.OK, response_model=Customer)
async def get_customer_by_cd(cd_customer):
    database = DatabaseClient()
    print(f"GET /customers/{cd_customer}")
    queried_customer = database() \
        .query(Customers) \
        .filter_by(cd_customer=cd_customer) \
        .first()
    return queried_customer


@app.get("/customers/", status_code=HTTPStatus.OK)
async def get_customers(sg_state: str = None):
    print(f"GET /customers/?{sg_state=}")
    database = DatabaseClient()
    customers_table = Customers()
    with database.engine.connect() as conn:
        results = conn.execute(customers_table.select())
    return results

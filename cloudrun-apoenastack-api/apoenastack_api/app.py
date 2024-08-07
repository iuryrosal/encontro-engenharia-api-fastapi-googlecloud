from fastapi import FastAPI, Request
from http import HTTPStatus
from apoenastack_api.schemas import Message, Customer
from apoenastack_api.database.models import Customers
from apoenastack_api.database.database_client import DatabaseClient

app = FastAPI()
database_session = DatabaseClient()


@app.get("/health_check", status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {"message": "API Activated!"}


@app.get("/customers/{cd_customer}", status_code=HTTPStatus.OK, response_model=Customer)
async def get_customer_by_cd(cd_customer):
    queried_customer = database_session() \
                        .query(Customers) \
                        .filter_by(cd_customer=cd_customer) \
                        .first()
    return queried_customer


@app.get("/customers/", status_code=HTTPStatus.OK, response_model=list[Customer])
async def get_customers(limit: int = 10, sg_state: str = None):
    if sg_state:
        queried_customers = database_session() \
                        .query(Customers) \
                        .filter_by(sg_state=sg_state) \
                        .limit(limit)
    else:
        queried_customers = database_session() \
                            .query(Customers) \
                            .limit(limit)
    return queried_customers

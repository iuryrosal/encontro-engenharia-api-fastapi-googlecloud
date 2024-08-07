from pydantic import BaseModel
from datetime import date


class Message(BaseModel):
    message: str


class Customer(BaseModel):
    cd_customer: str
    nm_customer: str
    st_email: str
    st_phone: str
    sg_state: str
    dt_birth: date

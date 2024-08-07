from sqlalchemy import Column, Date, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customers(Base):
    __tablename__ = 'customers'
    cd_customer = Column(String(256), primary_key=True)
    nm_customer = Column(String(135))
    st_email = Column(String(135))
    st_phone = Column(String(135))
    sg_state = Column(String(2))
    dt_birth = Column(Date)

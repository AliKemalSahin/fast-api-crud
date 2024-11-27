from sqlmodel import SQLModel, Field
from typing import Optional

class Customer(SQLModel, table=True):
    customer_id: int = Field(primary_key=True)
    customer_fname: str
    customer_lname: str
    customer_email: str
    customer_password: str
    customer_street: str
    customer_city: str
    customer_state: str
    customer_zipcode: str

class CustomerLNameUpdate(SQLModel):
    customer_lname: str
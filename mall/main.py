from fastapi import FastAPI
from mall.database import engine
from mall.routers import customers
from sqlmodel import SQLModel

app = FastAPI()

app.include_router(customers.router)

@app.on_event("startup")
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
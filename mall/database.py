import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()  # take environment variables from .env.
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
# print(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine) # table=true olan bütün veritabanları yaratılıyor 

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()
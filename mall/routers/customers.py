from fastapi import APIRouter, status, Depends, HTTPException
from mall.models import Customer, CustomerLNameUpdate
from mall.database import get_db, engine
from sqlmodel import Session, select
from typing import List
import pandas as pd
import bcrypt

router = APIRouter()

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

@router.post("/insert-customers/")
def insert_customers(request: Customer, session: Session = Depends(get_db)):
    url = "https://raw.githubusercontent.com/erkansirin78/datasets/master/retail_db/customers.csv"
    try:
        df = pd.read_csv(url, names=[
            "customer_id", "customer_fname", "customer_lname", 
            "customer_email", "customer_password", 
            "customer_street", "customer_city", 
            "customer_state", "customer_zipcode"
        ],
        header=0
        )
        first_10_records = df.head(10)

        for _, row in first_10_records.iterrows():
            hashed_password = hash_password(row["customer_password"])
            customer = Customer(
                customer_id=row["customer_id"],
                customer_fname=row["customer_fname"],
                customer_lname=row["customer_lname"],
                customer_email=row["customer_email"],
                customer_password=hashed_password,
                customer_street=row["customer_street"],
                customer_city=row["customer_city"],
                customer_state=row["customer_state"],
                customer_zipcode=row["customer_zipcode"]
            )
            session.add(customer)

        session.commit()
        return {"message": "First 10 records inserted successfully."}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/customers")
async def get_all(session: Session = Depends(get_db)):
    with session:
        customers = session.exec(
            select(Customer)).all()
        return customers
    
@router.put("/updateLastName", status_code=status.HTTP_202_ACCEPTED)
async def updateLastName(request: CustomerLNameUpdate, session: Session = Depends(get_db)):
    with session:
          customer8 = session.get(Customer, 8)
          if not customer8:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail=f"Customer with id = 8 has not found.")

          update_data = request.dict(exclude_unset=True)
          if "customer_lname" in update_data:
              customer8.customer_lname = update_data["customer_lname"]
          session.add(customer8)
          session.commit()
          session.refresh(customer8)
          return {"message": "Customer updated successfully", 
                  "customer smith updated last name": customer8.customer_lname}


@router.delete("/customer/{id}", status_code=status.HTTP_200_OK)
async def delete_customer(id: int, session: Session = Depends(get_db)):
    with session:
        one_customer = session.get(Customer, id)
        if not one_customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Customer with {id} has not found.")
        session.delete(one_customer)
        session.commit()
        return {f"Customer: {id} deleted."}


@router.get("/getCaguas", status_code=status.HTTP_200_OK)
async def getCaguas(session: Session = Depends(get_db)):
    with session:
        customers = session.exec(
            select(Customer).where(Customer.customer_city == "Caguas")).all()
        return customers

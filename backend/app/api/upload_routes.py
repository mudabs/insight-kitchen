from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/upload",
    tags=["CSV Upload"]
)

@router.post("/")
async def upload_csv(file: UploadFile = File(...),
                     db: Session = Depends(get_db)):
    """
    Upload and store restaurant CSV data.

    FLOW:
    CSV Upload
        ↓
    pandas DataFrame
        ↓
    Database insertion
    """

    try:
        # Read the stream once. UploadFile.file behaves like a cursor.
        df = pd.read_csv(file.file)
        inserted_orders = 0
        inserted_items = 0

        for _, row in df.iterrows():
            #Check if order already exists
            existing_order = db.query(Order).filter(
                Order.order_id == str(row["order_id"])
            ).first()

            #Create order only if it doesn't exist
            if not existing_order:
                new_order = Order(
                    order_id=str(row["order_id"]),
                    timestamp=pd.to_datetime(row["timestamp"]),
                    total_amount=row["total_amount"]
                )
                db.add(new_order)
                db.flush()
                inserted_orders += 1
            else:
                new_order = existing_order
            
            #Create order item
            new_item = OrderItem(
                order_id=new_order.id,
                item_name=row["item_name"],
                quantity=row["quantity"],
                price=row["price"]
            )
            db.add(new_item)
            inserted_items += 1

        db.commit()
        return {
            "message": "CSV uploaded successfully",
            "orders_inserted": inserted_orders,
            "items_inserted": inserted_items
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

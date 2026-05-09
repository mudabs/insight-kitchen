# FastAPI routing tool
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.order import Order
from app.schemas.order_schema import OrderCreate, OrderResponse 

#Create router
router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

@router.post("/", response_model = OrderResponse)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new restaurant order.

    FLOW:
    Request JSON
        ↓
    Pydantic validation
        ↓
    SQLAlchemy ORM object
        ↓
    PostgreSQL insert
    """
    #Create ORM object
    new_order = Order(
        order_id=order.order_id,
        timestamp=order.timestamp,
        total_amount=order.total_amount
    )

    #Add to database session
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """
    Retrieve all restaurant orders.
    """
    orders = db.query(Order).all()
    return orders
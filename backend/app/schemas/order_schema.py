#Used for timestamps
from datetime import datetime

#Base schema library
from pydantic import BaseModel

class OrderCreate(BaseModel):
    """
    Schema for creating a new order.

    Pydantic validates incoming request data automatically.
    """
    order_id: str
    timestamp: datetime
    total_amount: float

class OrderResponse(BaseModel):
    """
    Schema for returning order data to clients.
    """
    id: int
    order_id: str
    timestamp: datetime
    total_amount: float

    class Config:
        from_attributes = True
        #This class tells Pydantic to read data from ORM models (like SQLAlchemy) when creating response objects.
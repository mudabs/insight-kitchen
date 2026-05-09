#SQLAlchemy column types
from sqlalchemy import Column, Integer, String, Float, DateTime

#Import Base class
from app.database.database import Base

#Create Order table model
class Order(Base):
    #Database Table name
    __tablename__="orders"

    #Primary key
    id = Column(Integer, primary_key=True, index=True)

    #External order ID from restaurant system
    order_id = Column(String, nullable=False)

    #Time order was placed
    timestamp = Column(DateTime, nullable=False)

    #Total order amount
    total_amount = Column(Float, nullable=False)

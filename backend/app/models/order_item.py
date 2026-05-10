# SQLAlchemy relationship tools
from sqlalchemy import Column, Integer, String, Float, ForeignKey

# ORM relationship helper
from sqlalchemy.orm import relationship

# Import Base
from app.database.database import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    # Primary key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign key to orders table
    order_id = Column(Integer, ForeignKey("orders.id"))

    # Item information
    item_name = Column(String, nullable=False)

    category = Column(String)

    quantity = Column(Integer, nullable=False)

    price = Column(Float, nullable=False)

    # Relationship back to Order
    order = relationship("Order", back_populates="items")
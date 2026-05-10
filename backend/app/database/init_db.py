#Import database engine and Base class
from app.database.database import engine
from app.database.database import Base

#Import models so SQLAlchemy recognizes them when creating tables
from app.models.order import Order
from app.models.order_item import OrderItem

#Create all database tables
Base.metadata.create_all(bind=engine)

print("Database initialized successfully")
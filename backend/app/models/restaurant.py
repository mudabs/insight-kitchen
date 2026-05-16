from sqlalchemy import Column, ForeignKey, Integer, String, Float
from app.database.database import Base
from sqlalchemy.orm import relationship    

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    name = Column(String, nullable=False)
    organization = relationship("Organization")
    location = Column(String)
from sqlalchemy import Column, Integer, String
from app.database.database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    # Clerk organization ID
    clerk_org_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)


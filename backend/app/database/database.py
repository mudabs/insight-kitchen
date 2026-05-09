#Loading environment variables from .env file
from dotenv import load_dotenv

#Used to access environment variables
import os

#SQLAlchemy engine creator
from sqlalchemy import create_engine

#Creates database sessions
from sqlalchemy.orm import sessionmaker

#Base class for database models
from sqlalchemy.orm import declarative_base

#Load variables from .env file
load_dotenv()

#Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
print("DATABASE URL:", DATABASE_URL)

#Create SQLAlchemy engine using the database URL
engine = create_engine(DATABASE_URL)

#Create database session factory
sessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

#Base class for all database models
Base = declarative_base()
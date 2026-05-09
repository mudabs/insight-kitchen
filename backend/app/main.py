from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.order import Order  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure model metadata is registered and tables are present at startup.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}
# from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.order import Order  # noqa: F401
from app.api.order_routes import router as order_router


# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Ensure model metadata is registered and tables are present at startup.
#     Base.metadata.create_all(bind=engine)
#     yield


app = FastAPI(
    title="Insight Kitchen API",
    version="1.0.0",
)  

app.include_router(order_router)

@app.get("/")
async def root():
    return {"message": "Insight Kitchen API is running!"}
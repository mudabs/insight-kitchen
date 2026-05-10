from fastapi import APIRouter, UploadFile, File
import pandas as pd
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/upload",
    tags=["CSV Upload"]
)

@router.post("/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload restaurant CSV data.

    This endpoint:
    1. Receives CSV file
    2. Reads into pandas DataFrame
    3. Returns preview data
    """

    #Read uploaded csv file
    df = pd.read_csv(file.file)

    #Convert first rows to JSON preview
    preview = df.head().to_dict(orient="records")

    return{
        "filename": file.filename,
        "columns": list(df.columns),
        "preview": preview
    }
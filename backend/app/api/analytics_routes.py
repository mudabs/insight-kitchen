from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database.dependencies import get_db
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/revenue-summary")
def get_revenue_summary(db: Session = Depends(get_db)):
    """
    Returns high-level restaurant revenue metrics.
    """

    #Total revenue across all orders
    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar() or 0.0

    #Total orders placed
    total_orders = db.query(
        func.count(Order.id)
    ).scalar() or 0
    
    #Average order value
    average_order_value = total_revenue / total_orders if total_orders > 0 else 0

    if total_orders and total_orders > 0:
        average_order_value = total_revenue / total_orders

    return {"revenue_summary": {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "average_order_value": average_order_value
    }}
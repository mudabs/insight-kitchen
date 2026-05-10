from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

# Database dependency
from app.database.dependencies import get_db

# ORM models
from app.models.order import Order
from app.models.order_item import OrderItem

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/revenue-summary")
def revenue_summary(db: Session = Depends(get_db)):
    """
    Returns high-level restaurant revenue metrics.
    """

    # Total revenue
    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    # Total orders
    total_orders = db.query(
        func.count(Order.id)
    ).scalar()

    # Average order value
    average_order_value = 0

    if total_orders and total_orders > 0:
        average_order_value = total_revenue / total_orders

    return {
        "total_revenue": round(total_revenue or 0, 2),
        "total_orders": total_orders,
        "average_order_value": round(average_order_value, 2)
    }

@router.get("/top-items")
def top_items(db: Session = Depends(get_db)):
    """
    Returns best-selling menu items.
    """

    results = (
        db.query(
            OrderItem.item_name,
            func.sum(OrderItem.quantity).label("total_quantity")
        )
        .group_by(OrderItem.item_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .all()
    )

    return [
        {
            "item_name": item,
            "total_quantity": quantity
        }
        for item, quantity in results
    ]

@router.get("/hourly-sales")
def hourly_sales(db: Session = Depends(get_db)):
    """
    Analyze revenue by hour of day.
    """

    results = (
        db.query(
            func.extract("hour", Order.timestamp).label("hour"),
            func.sum(Order.total_amount).label("revenue")
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    return [
        {
            "hour": int(hour),
            "revenue": float(revenue)
        }
        for hour, revenue in results
    ]
from app.services.insight_service import generate_business_insights

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

# Database dependency
from app.database.dependencies import get_db

# ORM models
from app.models.order import Order
from app.models.order_item import OrderItem
import pandas as pd

from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)
from app.services.auth_service import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/revenue-summary")
def revenue_summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
def top_items(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
def hourly_sales(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
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
            "revenue": round(float(revenue),2)
        }
        for hour, revenue in results
    ]

@router.get("/basket-analysis")
def basket_analysis(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Discover items commonly purchased together.
    """

    # Fetch all order items
    items = db.query(
        OrderItem.order_id,
        OrderItem.item_name
    ).all()

    # Convert query results into DataFrame
    df = pd.DataFrame(
        items,
        columns=["order_id", "item_name"]
    )

    # Create basket matrix
    basket = (
        df.groupby(["order_id", "item_name"])
        .size()
        .unstack(fill_value=0)
    )

    # Convert counts to binary values
    basket = (basket > 0).astype(int)

    # Generate frequent itemsets
    frequent_itemsets = apriori(
        basket,
        min_support=0.05,
        use_colnames=True
    )

    # Generate association rules
    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1
    )

    # Sort strongest associations
    rules = rules.sort_values(
        by="lift",
        ascending=False
    )

    # Return top rules
    results = []

    for _, row in rules.head(10).iterrows():

        results.append({
            "if_customer_buys": list(row["antecedents"]),
            "they_also_buy": list(row["consequents"]),
            "support": round(row["support"], 2),
            "confidence": round(row["confidence"], 2),
            "lift": round(row["lift"], 2)
        })

    return results

@router.get("/business-insights")
def business_insights(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Generate high-level business insights.
    """
    insights = generate_business_insights(db)
    return {"insights": insights}

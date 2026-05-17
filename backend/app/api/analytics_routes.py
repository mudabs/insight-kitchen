from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

import pandas as pd

from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)

# Database dependency
from app.database.dependencies import get_db

# ORM models
from app.models.order import Order
from app.models.order_item import OrderItem

# Auth + tenant services
from app.services.auth_service import (
    get_current_user
)

from app.services.tenant_service import (
    get_current_organization,
    get_restaurant_ids_for_organization
)

# Insights service
from app.services.insight_service import (
    generate_business_insights
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


# -----------------------------------
# Revenue Summary
# -----------------------------------

@router.get("/revenue-summary")
def revenue_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    organization = get_current_organization(
        db,
        current_user
    )

    restaurant_ids = (
        get_restaurant_ids_for_organization(
            db,
            organization.id
        )
    )

    # Total revenue
    total_revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .filter(
            Order.restaurant_id.in_(restaurant_ids)
        )
        .scalar()
    )

    # Total orders
    total_orders = (
        db.query(
            func.count(Order.id)
        )
        .filter(
            Order.restaurant_id.in_(restaurant_ids)
        )
        .scalar()
    )

    average_order_value = 0

    if total_orders and total_orders > 0:
        average_order_value = (
            total_revenue / total_orders
        )

    return {
        "organization": organization.name,
        "total_revenue": round(total_revenue or 0, 2),
        "total_orders": total_orders,
        "average_order_value": round(
            average_order_value,
            2
        )
    }


# -----------------------------------
# Top Selling Items
# -----------------------------------

@router.get("/top-items")
def top_items(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    organization = get_current_organization(
        db,
        current_user
    )

    restaurant_ids = (
        get_restaurant_ids_for_organization(
            db,
            organization.id
        )
    )

    results = (
        db.query(
            OrderItem.item_name,
            func.sum(
                OrderItem.quantity
            ).label("total_quantity")
        )
        .join(
            Order,
            OrderItem.order_id == Order.id
        )
        .filter(
            Order.restaurant_id.in_(restaurant_ids)
        )
        .group_by(
            OrderItem.item_name
        )
        .order_by(
            func.sum(
                OrderItem.quantity
            ).desc()
        )
        .all()
    )

    return [
        {
            "item_name": item,
            "total_quantity": quantity
        }
        for item, quantity in results
    ]


# -----------------------------------
# Hourly Sales
# -----------------------------------

@router.get("/hourly-sales")
def hourly_sales(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    organization = get_current_organization(
        db,
        current_user
    )

    restaurant_ids = (
        get_restaurant_ids_for_organization(
            db,
            organization.id
        )
    )

    results = (
        db.query(
            func.extract(
                "hour",
                Order.timestamp
            ).label("hour"),

            func.sum(
                Order.total_amount
            ).label("revenue")
        )
        .filter(
            Order.restaurant_id.in_(restaurant_ids)
        )
        .group_by("hour")
        .order_by("hour")
        .all()
    )

    return [
        {
            "hour": int(hour),
            "revenue": round(
                float(revenue),
                2
            )
        }
        for hour, revenue in results
    ]


# -----------------------------------
# Basket Analysis
# -----------------------------------

@router.get("/basket-analysis")
def basket_analysis(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    organization = get_current_organization(
        db,
        current_user
    )

    restaurant_ids = (
        get_restaurant_ids_for_organization(
            db,
            organization.id
        )
    )

    items = (
        db.query(
            OrderItem.order_id,
            OrderItem.item_name
        )
        .join(
            Order,
            OrderItem.order_id == Order.id
        )
        .filter(
            Order.restaurant_id.in_(restaurant_ids)
        )
        .all()
    )

    # Prevent empty dataframe crashes
    if not items:

        return {
            "message": "No basket data available."
        }

    df = pd.DataFrame(
        items,
        columns=[
            "order_id",
            "item_name"
        ]
    )

    basket = (
        df.groupby(
            ["order_id", "item_name"]
        )
        .size()
        .unstack(fill_value=0)
    )

    basket = (
        basket > 0
    ).astype(int)

    frequent_itemsets = apriori(
        basket,
        min_support=0.05,
        use_colnames=True
    )

    if frequent_itemsets.empty:

        return {
            "message": "No frequent itemsets found."
        }

    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=1
    )

    rules = rules.sort_values(
        by="lift",
        ascending=False
    )

    results = []

    for _, row in rules.head(10).iterrows():

        results.append({
            "if_customer_buys": list(
                row["antecedents"]
            ),
            "they_also_buy": list(
                row["consequents"]
            ),
            "support": round(
                row["support"],
                2
            ),
            "confidence": round(
                row["confidence"],
                2
            ),
            "lift": round(
                row["lift"],
                2
            )
        })

    return results


# -----------------------------------
# Business Insights
# -----------------------------------

@router.get("/business-insights")
def business_insights(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    organization = get_current_organization(
        db,
        current_user
    )

    restaurant_ids = (
        get_restaurant_ids_for_organization(
            db,
            organization.id
        )
    )

    insights = generate_business_insights(
        db,
        restaurant_ids
    )

    return {
        "organization": organization.name,
        "insights": insights
    }
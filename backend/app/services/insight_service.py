from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.order import Order
from app.models.order_item import OrderItem


def generate_business_insights(db: Session):

    insights = []

    # -----------------------------------
    # Peak Revenue Hour
    # -----------------------------------

    hourly_sales = (
        db.query(
            func.extract("hour", Order.timestamp).label("hour"),
            func.sum(Order.total_amount).label("revenue")
        )
        .group_by("hour")
        .all()
    )

    if hourly_sales:

        peak_hour = max(
            hourly_sales,
            key=lambda x: x.revenue
        )

        insights.append(
            f"Peak revenue occurs around {int(peak_hour.hour)}:00 with approximately ${round(float(peak_hour.revenue), 2)} in sales."
        )

    # -----------------------------------
    # Top Selling Item
    # -----------------------------------

    top_item = (
        db.query(
            OrderItem.item_name,
            func.sum(OrderItem.quantity).label("quantity")
        )
        .group_by(OrderItem.item_name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .first()
    )

    if top_item:

        insights.append(
            f"The best-selling menu item is {top_item.item_name} with {int(top_item.quantity)} total orders."
        )

    # -----------------------------------
    # Average Order Value
    # -----------------------------------

    total_revenue = db.query(
        func.sum(Order.total_amount)
    ).scalar()

    total_orders = db.query(
        func.count(Order.id)
    ).scalar()

    if total_orders and total_orders > 0:

        average_order_value = total_revenue / total_orders

        insights.append(
            f"The average customer order value is ${round(float(average_order_value), 2)}."
        )

    # -----------------------------------
    # Revenue Concentration
    # -----------------------------------

    evening_revenue = (
        db.query(
            func.sum(Order.total_amount)
        )
        .filter(
            func.extract("hour", Order.timestamp) >= 17
        )
        .scalar()
    )

    if evening_revenue and total_revenue:

        percentage = (
            evening_revenue / total_revenue
        ) * 100

        insights.append(
            f"Evening hours contribute approximately {round(float(percentage), 1)}% of total revenue."
        )

    return insights
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.models.product import Product
from app.models.order import Order
from app.schemas.order import OrderCreate
from app.tasks.order_tasks import process_order


def create_order(db: Session, order_in: OrderCreate) -> Order:
    try:
        # Lock product row
        stmt = (
            select(Product)
            .where(Product.id == order_in.product_id)
            .with_for_update()
        )
        product = db.execute(stmt).scalar_one_or_none()

        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        if product.stock < order_in.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        # Reduce stock
        product.stock -= order_in.quantity

        # Create order
        order = Order(
            product_id=order_in.product_id,
            quantity=order_in.quantity
        )

        db.add(order)
        db.commit()
        db.refresh(order)

        # Trigger async task for order processing
        process_order.delay(order.id)
        
        return order

    except:
        db.rollback()
        raise

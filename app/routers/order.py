from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order
from app.tasks.celery_app import send_order_task

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order_endpoint(
    order_in: OrderCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new order with race condition handling for stock management.
    
    Handles concurrent requests using database-level transaction isolation
    to ensure stock consistency. Only one order succeeds if multiple requests
    attempt to purchase the last item simultaneously.
    """
    order = create_order(db, order_in)
    
    # Trigger Celery task for async processing
    send_order_task.delay(order.id)
    
    return order


@router.get("/", response_model=list[OrderResponse])
def get_orders(db: Session = Depends(get_db)):
    """
    Retrieve all orders.
    """
    return db.query(Order).all()


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific order by ID.
    """
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.order import OrderCreate
from app.services.order_service import create_order

router = APIRouter()


@router.post("/")
def create_order_endpoint(
    order_in: OrderCreate,
    db: Session = Depends(get_db)
):
    return create_order(db, order_in)

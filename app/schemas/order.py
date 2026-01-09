from pydantic import BaseModel, Field
from datetime import datetime

class OrderCreate(BaseModel):
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=2)

class OrderResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True

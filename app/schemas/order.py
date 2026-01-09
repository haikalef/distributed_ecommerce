from pydantic import BaseModel, Field

class OrderCreate(BaseModel):
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., gt=0, example=2)

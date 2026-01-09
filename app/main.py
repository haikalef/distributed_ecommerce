from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import product, order
from app.routers import product as product_router
from app.routers import order as order_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router.router)
app.include_router(order_router.router)

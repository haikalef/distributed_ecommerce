from fastapi import FastAPI
from app.core.database import engine, Base
from app.models import product, order
from app.routers import product as product_router
from app.routers import order as order_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Distributed E-Commerce Order System", version="1.0.0")

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint to verify API is running"""
    return {"status": "healthy"}

# Include routers
app.include_router(product_router.router)
app.include_router(order_router.router)

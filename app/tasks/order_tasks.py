import time
from app.core.celery_app import celery_app

@celery_app.task(name="process_order")
def process_order(order_id: int):
    time.sleep(5)
    print(f"Order #{order_id} Processed")

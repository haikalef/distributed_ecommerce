from celery import Celery

celery_app = Celery(
    "distributed_ecommerce",
    broker="redis://redis:6380/0",
    backend="redis://redis:6380/0",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Jakarta",
    enable_utc=True,
)

import app.tasks.order_tasks

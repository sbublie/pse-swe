from celery import Celery
import time

# Create a Celery instance
app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',
    backend='rpc://'  # Memory-Backend
)
@app.task
def order_from_china(product, quantity):
    time.sleep(12)  
    return f"谢谢 for ordering {quantity} {product}s"


@app.task
def order_from_korea(product, quantity):
    time.sleep(2)
    order_from_china.delay(product, quantity)
    return f"감사합니다 for ordering {quantity} {product}s"


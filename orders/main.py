from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from starlette.requests import Request
import requests, time

from models import Order, redis


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def format(pk: str):
    order = Order.get(pk)

    return {
        "id": order.pk,
        "product_id": order.product_id,
        "price": order.price,
        "fee": order.fee,
        "total": order.total,
        "quantity": order.quantity,
        "status": order.status,
    }


@app.get("/orders")
def all():
    return [format(pk) for pk in Order.all_pks()]


@app.post("/orders")
async def create_order(request: Request, tasks: BackgroundTasks):
    body = await request.json()

    product = requests.get(f"http://localhost:8000/products/{body['id']}").json()
    print(product)
    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=0.2 * product["price"],
        total=1.2 * product["price"],
        quantity=body["quantity"],
        status="pending",
    )
    order.save()
    redis.xadd("order_completed", order.dict(), "*")
    tasks.add_task(complete_order, order)
    return order


def complete_order(order: Order):
    time.sleep(2)
    order.status = "completed"
    order.save()


@app.get("/orders/{pk}")
def get_order(pk: str):
    order = Order.get(pk)
    redis.xadd("refund_order", order.dict(), "*")
    return order


@app.delete("/orders/{pk}")
def delete_order(pk: str):
    return Order.delete(pk)

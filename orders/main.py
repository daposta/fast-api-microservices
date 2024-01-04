from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import HashModel, get_redis_connection
from starlette.requests import Request
import requests, time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-13265.c242.eu-west-1-2.ec2.cloud.redislabs.com",
    port=13265,
    decode_responses=True,
    password="CNoroCPSNMEXkr1T2XTiQGTDgVOQmz4K",
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending/completed/refunded

    class Meta:
        database = redis


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

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=0.2 * product["price"],
        total=1.2 * product["price"],
        quantity=body["quantity"],
        status="pending",
    )
    order.save()
    tasks.add_task(complete_order, order)
    # complete_order(order)
    return order


def complete_order(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()


@app.get("/orders/{pk}")
def get_order(pk: str):
    order = Order.get(pk)
    return order


@app.delete("/orders/{pk}")
def delete_order(pk: str):
    return Order.delete(pk)

from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from redis_om import HashModel, get_redis_connection


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


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


@app.post("/products")
def create_product(product: Product):
    return product.save()


@app.get("/products/{pk}")
def get_product(pk: str):
    product = Product.get(pk)
    return product


@app.delete("/products/{pk}")
def delete_product(pk: str):
    return Product.delete(pk)

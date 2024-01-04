from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Product


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

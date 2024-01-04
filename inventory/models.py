from redis_om import HashModel, get_redis_connection
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

redis = get_redis_connection(
    host=os.getenv(
        "REDIS_HOST"
    ),  # "redis-13265.c242.eu-west-1-2.ec2.cloud.redislabs.com",
    port=os.getenv("PORT"),
    decode_responses=True,
    password=os.getenv("DB_PASS"),  # "CNoroCPSNMEXkr1T2XTiQGTDgVOQmz4K",
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

from redis_om import HashModel, get_redis_connection
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

redis = get_redis_connection(
    host=os.getenv(
        "REDIS_HOST"
    ),  # "redis-13265.c242.eu-west-1-2.ec2.cloud.redislabs.com",
    port=13265,
    decode_responses=True,
    password=os.getenv("DB_PASS"),  # "CNoroCPSNMEXkr1T2XTiQGTDgVOQmz4K",
)

# redis = get_redis_connection(
#     host="redis-13265.c242.eu-west-1-2.ec2.cloud.redislabs.com",
#     port=13265,
#     decode_responses=True,
#     password="CNoroCPSNMEXkr1T2XTiQGTDgVOQmz4K",
# )


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending/completed/refunded

    class Meta:
        database = redis

from redis_om import HashModel, get_redis_connection
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("PORT"),
    decode_responses=True,
    password=os.getenv("DB_PASS"),
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

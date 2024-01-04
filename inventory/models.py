from redis_om import HashModel, get_redis_connection

redis = get_redis_connection(
    host="redis-14779.c78.eu-west-1-2.ec2.cloud.redislabs.com",
    port=14779,
    decode_responses=True,
    password="1uRRQlteLfFKbUVLt5yx10jYcpj03xlk",
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis

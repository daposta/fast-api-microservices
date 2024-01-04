import time
from models import redis, Product


key = "order_completed"
group = "inventory-group"

try:
    redis.xgroup_create(key, group)
except:
    print("Group already exists")


while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]  # result[1][0][1]
                product = Product.get(obj["product_id"])
                if product and product.quantity >= int(obj["quantity"]):
                    product.quantity -= int(obj["quantity"])
                    product.save()
                    print("Product quantity updated")
                else:
                    redis.xadd("refund_order", obj, "*")
                    raise ValueError("Product not found")

    except Exception as e:
        print(str(e))
    time.sleep(1)

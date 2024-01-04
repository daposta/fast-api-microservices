from models import redis, Order
import time

key = "refund_order"
group = "order-group"

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
                obj = result[1][0][1]  # result[0][1][0][1]
                order = Order.get(obj["pk"])
                if order:
                    order.status = "refunded"
                    order.save()
                else:
                    redis.xadd("refund_order", obj, "*")
    except Exception as e:
        print(str(e))
    time.sleep(1)

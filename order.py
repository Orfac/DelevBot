from pymongo import MongoClient


class Order:
    def __init__(self, customer_id, description,
                 performer_id=-1):
        self.customer_id = customer_id
        self.description = description
        self.performer_id = performer_id

    def to_dict(self):
        order_dict = {
            'customer_id': self.customer_id,
            'description': self.description,
            'performer_id': self.performer_id,
        }

        return order_dict


def __get_orders():
    client = MongoClient()
    db = client['BotDB']
    orders = db['Orders']
    return orders


def add_order(order):
    orders = __get_orders()
    orders.insert_one(order.to_dict())


def delete_order(customer_id):
    orders = __get_orders()
    orders.remove({"customer_id": customer_id})


def take_order(customer_id, performer_id):
    orders = __get_orders()
    orders.update_one(
        {'customer_id': customer_id},
        {
            "$set": {'performer_id': performer_id}
        }
    )


def get_order(customer_id):
    orders = __get_orders()
    order_d = orders.find_one(
        {'customer_id': customer_id}
    )
    order_d.pop('_id', None)
    order = Order(**order_d)
    return order


def print_orders():
    orders = __get_orders()
    orders_collection = orders.find()
    for order in orders_collection:
        print(order)


def drop_orders():
    client = MongoClient()
    db = client['BotDB']
    orders = db['Orders']
    orders.drop()
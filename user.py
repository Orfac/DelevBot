from pymongo import MongoClient


# mongo db collection
def __get_users():
    client = MongoClient()
    db = client['BotDB']
    users = db['Users']
    return users


def get_users():
    users = __get_users()
    users_coll = users.find()
    list_users = []
    for user in users_coll:
        new_user = {'id': user['id'], "state": user['state']}
        list_users.append(new_user)
    return list_users


def get_users_ids(filter_id=None):
    users = get_users()
    list_ids = []
    for user in users:
        if user['id'] != filter_id:
            list_ids.append(user['id'])
    return list_ids


def add_new_user(new_id):
    users = __get_users()
    users.update_one(
        {"id": new_id},
        {
            "$setOnInsert": {"id": new_id, "state": "normal"}
        },
        upsert=True
    )


# this method is used only for debug
def print_users():
    users = __get_users()
    users_collection = users.find()
    for user in users_collection:
        print(user)


def set_state(user_id, state):
    users = __get_users()
    users.update_one(
        {"id": user_id},
        {
            "$set": {"id": user_id, "state": state}
        }
    )


def get_state(user_id):
    users = __get_users()
    user = users.find_one(
        {"id": user_id}
    )
    return user["state"]


def remove_user(user_id):
    users = __get_users()
    users.remove({"id": user_id})


def drop_users():

    client = MongoClient()
    db = client['BotDB']
    users = db['Users']
    users.drop()

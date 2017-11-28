from pymongo import MongoClient

# mongo_db collection
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
        new_user = {'id': user['id']}
        list_users.append(new_user)
    return list_users

def add_new_user(new_id):
    users = __get_users()
    users.update_one(
        {"id": new_id},
        {
            "$setOnInsert": {"id": new_id}
        },
        upsert=True
    )

# this method is used only for debug
def print_all_users():
    users = __get_users()
    users_collection = users.find()
    for user in users_collection:
        print(user)

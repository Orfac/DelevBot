from pymongo import MongoClient

def set_token(token):
    client = MongoClient()
    db = client['BotDB']
    token_coll = db['token']

    coll = {'value': token}
    token_coll.insert_one(coll)


# noinspection PyBroadException
def get_token():
    result = -1
    try:
        client = MongoClient()
        db = client['BotDB']
        token_coll = db['token']
        tokens = token_coll.find()
        for token_d in tokens:
            result = token_d['value']
    except Exception:
        pass
    return result

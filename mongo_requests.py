from config import *

def was_user(cid):
    return db.users.find_one(str(cid)) is not None and db.users.find_one(str(cid))['active'] == False

def is_user(cid):
    return db.users.find_one(str(cid)) is not None and db.users.find_one(str(cid))['active'] == True

def add_user(cid, usernames):
    users = db.users.find_one(str(cid))['users']

    users.extend(usernames)
    users = tuple(set(users))
    print(users)
    db.users.update_one({"_id": str(cid)}, {"$set": {"users": users}})

def remove_user(cid, usernames):
    users = db.users.find_one(str(cid))['users']
    users = tuple(set(users) - set(usernames))
    print(users)
    db.users.update_one({"_id": str(cid)}, {"$set": {"users": users}})

def get_users(cid):
    return db.users.find_one(str(cid))['users']

def set_context(cid, context):
    db.users.update_one({"_id": str(cid)}, {"$set": {"context": context}})

def get_context(cid):
    return db.users.find_one(str(cid))['context']
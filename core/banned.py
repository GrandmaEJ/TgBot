import json

def is_user_banned(user_id):
    with open('data/banned.json') as f:
        banned_users = json.load(f)
    return str(user_id) in banned_users
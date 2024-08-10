import json

def is_premium_user(user_id):
    with open('data/premium.json') as f:
        premium_users = json.load(f)
    return str(user_id) in premium_users
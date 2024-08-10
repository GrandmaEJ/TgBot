import json
import os

def add_new_user(user_id, name=None, username=None):
    if not os.path.exists('data/users.json'):
        with open('data/users.json', 'w') as f:
            json.dump({}, f)

    with open('data/users.json', 'r+') as f:
        users = json.load(f)
        if str(user_id) not in users:
            users[str(user_id)] = {
                "name": name,
                "username": username
            }
            f.seek(0)
            json.dump(users, f, indent=4)
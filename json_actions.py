import os, json

def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(file, data) -> None:
    with open(file, 'r') as f:
        current_data = json.load(f)
    current_data.update(data)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=4)

def save_data_user(file, user_data) -> None:
    with open(file, 'r', encoding='utf-8') as f:
        current_data = json.load(f)

    user_id = list(user_data.keys())[0]  
    if user_id in current_data:
        current_data[user_id]['region'] = user_data[user_id]['region']
        current_data[user_id]['city'] = user_data[user_id]['city']
        current_data[user_id]['language'] = user_data[user_id]['language']
    else:
        current_data.update(user_data)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(current_data, f, indent=4)
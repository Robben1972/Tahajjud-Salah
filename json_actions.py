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
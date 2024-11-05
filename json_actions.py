import os, json

def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(file, data) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
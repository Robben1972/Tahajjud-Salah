from json_actions import load_data

def sort_data():
    data = load_data('Json/user_info.json')

    sorted_users = sorted(data.values(), key=lambda x: x['all_prays'], reverse=True)

    top_users = sorted_users[:5]
    b: str = ''
    for user in top_users:
        b += f"{user['fullname']} -> {user['all_prays']}\n"
    return b
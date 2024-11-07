from bs4 import BeautifulSoup
import requests
from json_actions import load_data, save_data
from variables import city_data
import schedule
import time

user_info = load_data('Json/user_info.json')

def update_user_info():
    global user_info
    user_info = load_data('Json/user_info.json')

def fetch_and_save_data():
    data = {}
    update_user_info()
    for i in user_info:
        response = requests.get(f"https://namozvaqti.uz/shahar/{user_info[i]['city'].lower()}")
        soup = BeautifulSoup(response.content, 'html.parser')
        link = str(soup.find_all('script')[-1])
        data[i] = link[link.find('const times')+25 : link.find('const times')+30]
    save_data('Json/times.json', data)

schedule.every().day.at("00:00").do(fetch_and_save_data)

while True:
    schedule.run_pending()
    time.sleep(1)

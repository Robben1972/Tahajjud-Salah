import asyncio
import logging
import sys
from bs4 import BeautifulSoup
import requests
from json_actions import load_data, save_data
from variables import city_data
from aiogram import Bot
from variables import TOKEN

bot = Bot(token=TOKEN)

# Load user information
user_info = load_data('Json/user_info.json')

def update_user_info():
    global user_info
    user_info = load_data('Json/user_info.json')

async def fetch_and_save_data():
    data = {}
    update_user_info()
    for i in user_info:
        response = requests.get(city_data[user_info[i]['language']][user_info[i]['region']][user_info[i]['city']])
        soup = BeautifulSoup(response.content, 'html.parser')
        link = str(soup.find_all('script')[-1])
        data[i] = link[link.find('const times')+25 : link.find('const times')+30]
    save_data('Json/times.json', data)

async def periodic_check_24():
    while True:
        await fetch_and_save_data()
        await asyncio.sleep(86400)
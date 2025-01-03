import asyncio
import time
from json_actions import load_data
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from variables import TOKEN, trs

bot = Bot(token=TOKEN)

async def update_user_info():
    user_data = load_data('Json/times.json')
    current_time = time.strftime("%H:%M", time.localtime())
    for user_id, user_time in user_data.items():
        if current_time == user_time:
            await send_notification(user_id)

async def send_notification(user_id):
    user_data = load_data('Json/user_info.json')
    buttons=[
                InlineKeyboardButton(text='Yes', callback_data='pray_yes'),
                InlineKeyboardButton(text='No', callback_data='pray_no')
            ],
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await bot.send_message(
        user_id,
        trs["prayed"][user_data[str(user_id)]['language']],
        reply_markup=keyboard
    )

async def periodic_check():
    while True:
        await update_user_info()
        await asyncio.sleep(60)

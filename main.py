import asyncio
import logging
import sys
import random

from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode, ContentType
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.types import Message
from variables import TOKEN, trs, prays
from daily_send import periodic_check
from scrapping_data import periodic_check_24
from json_actions import save_data, load_data, save_data_user
from reply_markups import generate_region_buttons, language_selector, generate_city_buttons, settings_buttons
from gemeni import generate_answer
from scrapping_data import fetch_and_save_data
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup





bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()

user_data = load_data("Json/user_info.json")

def update():
    global user_data
    user_data = load_data("Json/user_info.json")


class GettingInfo(StatesGroup):
    user_id = State()
    fullname = State()
    language = State()
    region = State()
    city = State()

class Chat_AI(StatesGroup):
    user_id = State()
    chatting = State()

@dp.message(lambda message: any(word in message.text for word in [trs['settings']['uz'][0], trs['settings']['ar'][0], trs['settings']['уз'][0]]))
async def change_lang(message: Message, state: FSMContext):
    await message.answer(f"{trs['greeting']['uz']}\n {trs['greeting']['уз']} \n {trs['greeting']['ar']}", reply_markup=language_selector())
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(fullname=message.from_user.full_name)
    await state.set_state(GettingInfo.language)

@dp.message(lambda message: message.text in [trs['back']['uz'], trs['back']['уз'], trs['back']['ar']], Chat_AI.chatting)
async def back_to_greeting(message: Message, state: FSMContext) -> None:
    await state.clear()  # Clear the Chat_AI state
    await message.answer(f"{trs['come_back'][user_data[str(message.from_user.id)]['language']]}", reply_markup=settings_buttons(user_data[str(message.from_user.id)]['language']))
    await state.set_state(GettingInfo.language)

@dp.message(F.content_type == ContentType.TEXT, Chat_AI.chatting)
async def chatting(message: Message, state: FSMContext):
    a = await generate_answer(message.text)
    await message.answer(
    f'{a}', 
    reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=trs['back'][user_data[str(message.from_user.id)]['language']])]], resize_keyboard=True, one_time_keyboard=True)
)

@dp.message(lambda message: any(word in message.text for word in [trs['settings']['uz'][1], trs['settings']['ar'][1], trs['settings']['уз'][1]]))
async def chat_ai(message: Message, state: FSMContext):
    await message.answer(trs['ai'][user_data[str(message.from_user.id)]['language']])
    await state.update_data(user_id=message.from_user.id)
    await state.set_state(Chat_AI.chatting)

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if str(message.from_user.id) not in user_data:
        await message.answer(f"{trs['greeting']['uz']}\n {trs['greeting']['уз']} \n {trs['greeting']['ar']}", reply_markup=language_selector())
        await state.update_data(user_id=message.from_user.id)
        await state.update_data(fullname=message.from_user.full_name)
        await state.set_state(GettingInfo.language)
    else:
        await message.answer(f"{trs['come_back'][user_data[str(message.from_user.id)]['language']]}", reply_markup=settings_buttons(user_data[str(message.from_user.id)]['language']))


@dp.callback_query(lambda c: c.data and c.data.startswith("pray_"))
async def process_sleep_response(callback_query: types.CallbackQuery):
    response = callback_query.data.split("_")[1]
    if response == "yes":
        await bot.send_message(callback_query.from_user.id, text=random.choice(prays[user_data[str(callback_query.from_user.id)]['language']]['yes']))
        user_data[str(callback_query.from_user.id)]['all_prays'] += 1
        user_data[str(callback_query.from_user.id)]['prays_in_row'] += 1
    else:
        await bot.send_message(callback_query.from_user.id, text=random.choice(prays[user_data[str(callback_query.from_user.id)]['language']]['no']))
        user_data[str(callback_query.from_user.id)]['prays_in_row'] = 0
    save_data("Json/user_info.json", user_data)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)

@dp.callback_query()
async def language_callback(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    await state.update_data(language=callback_query.data)
    await callback_query.message.delete()
    data = await state.get_data()
    await callback_query.message.answer(f"{trs['region'][data['language']]}", reply_markup=generate_region_buttons(data['language']))
    await state.set_state(GettingInfo.region)



@dp.message(F.content_type == ContentType.TEXT, GettingInfo.region)
async def city(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if message.text == trs['back'][data['language']]:
        await message.answer(f"{trs['greeting']['uz']}\n {trs['greeting']['уз']} \n {trs['greeting']['ar']}", reply_markup=language_selector())
    else:
        await state.update_data(region=message.text)
        await state.set_state(GettingInfo.city)
        data = await state.get_data()
        await message.answer(f"{trs['city'][data['language']]}", reply_markup=generate_city_buttons(data['language'], data['region']))

@dp.message(F.content_type == ContentType.TEXT, GettingInfo.city)
async def save_datas(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if message.text == trs['back'][data['language']]:
        await state.set_state(GettingInfo.region)
        await message.answer(f"{trs['region'][data['language']]}", reply_markup=generate_region_buttons(data['language']))
    else:
        await state.update_data(city=message.text)
        data = await state.get_data()
        user_data = {
            str(data['user_id']): {
                'fullname': data['fullname'],
                'language': data['language'],
                'region': data['region'],
                'city': data['city'],
                'usernmae': message.from_user.username,
                'all_prays': 0,
                'prays_in_row': 0
            }
        }
        save_data_user('Json/user_info.json', user_data)
        await state.clear()
        update()
        await fetch_and_save_data()
        await message.answer(f"{trs['thanks'][data['language']]}", reply_markup=settings_buttons(user_data[str(message.from_user.id)]['language']))



async def main() -> None:
    asyncio.create_task(periodic_check())
    # asyncio.create_task(periodic_check_24())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
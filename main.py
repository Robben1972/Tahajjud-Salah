import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode, ContentType
from aiogram.types import ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.types import Message
from variables import TOKEN, trs, city_data
from daily_send import periodic_check
from scrapping_data import periodic_check_24
from json_actions import save_data, load_data
from reply_markups import generate_region_buttons, language_selector, generate_city_buttons
from gemeni import generate_answer


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



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if str(message.from_user.id) not in user_data:
        await message.answer(f"{trs['greeting']['uz']}\n {trs['greeting']['уз']} \n {trs['greeting']['ar']}", reply_markup=language_selector())
        await state.update_data(user_id=message.from_user.id)
        await state.update_data(fullname=message.from_user.full_name)
        await state.set_state(GettingInfo.language)
    else:
        await message.answer(f"{trs['come_back'][user_data[str(message.from_user.id)]['language']]}", reply_markup=ReplyKeyboardRemove())


@dp.callback_query(lambda c: c.data and c.data.startswith("pray_"))
async def process_sleep_response(callback_query: types.CallbackQuery):
    response = callback_query.data.split("_")[1]
    if response == "yes":
        text = await generate_answer('Generate good words for the person who prayed tahajjud today. Keep it simple and small, return just one sentence. You can also give small hadith or Quran ayahs')
        await bot.send_message(callback_query.from_user.id, text=text)
    else:
        text = await generate_answer("Generate a good words for the person who tries to pray tahajjud but today overslept and couldn't pray it. Return simple and small motivation one sentence for him")
        await bot.send_message(callback_query.from_user.id, text=text)
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
            data['user_id']: {
                'fullname': data['fullname'],
                'language': data['language'],
                'region': data['region'],
                'city': data['city']
            }
        }
        save_data('Json/user_info.json', user_data)
        await state.clear()
        update()
        await message.answer(f"{trs['thanks'][data['language']]}", reply_markup=ReplyKeyboardRemove())



async def main() -> None:
    asyncio.create_task(periodic_check())
    # asyncio.create_task(periodic_check_24())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
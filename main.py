import asyncio
import logging
import sys

from environs import Env
from aiogram import Bot, Dispatcher, html
from aiogram.fsm.state import StatesGroup, State
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from variables import user_data, TOKEN
from reply_markups import generate_region_buttons

dp = Dispatcher()


class GettingInfo(StatesGroup):
    user_id = State()
    fullname = State()
    region = State()
    city = State()



@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    if str(message.from_user.id) not in user_data:
        await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!", reply_markup=generate_region_buttons())
        await state.update_data(user_id=message.from_user.id)
        await state.update_data(fullname=message.from_user.full_name)
        await state.set_state(GettingInfo.region)
    else:
        await message.answer(f"Welcome back to the Tahajjud Salah Bot! ")

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
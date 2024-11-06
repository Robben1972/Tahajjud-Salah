from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton 
from variables import city_data
def generate_region_buttons():
    region_button = [[]]
    count = 0
    for i in city_data['3']:
            if count % 2 == 0:
                region_button[-1].append(KeyboardButton(text=i))
                count += 1
            else:
                region_button.append([KeyboardButton(text=i)])
                count = 0
    keyboard = ReplyKeyboardMarkup(keyboard=region_button, resize_keyboard=True, one_time_keyboard=True)
    return keyboard    

def language_selector():
     return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='O\'zbek', callback_data='uz'),
                InlineKeyboardButton(text='العربية', callback_data='ar'),
                InlineKeyboardButton(text='Узбек', callback_data='уз')
            ],
        ]) 

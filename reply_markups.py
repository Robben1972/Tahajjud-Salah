from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton 
from variables import city_data, trs
def generate_region_buttons(language: str):
    region_button = [[]]
    count = 0
    for i in city_data[language]:
            if count % 2 == 0:
                region_button[-1].append(KeyboardButton(text=i))
                count += 1
            else:
                region_button.append([KeyboardButton(text=i)])
                count = 0
    region_button.append([KeyboardButton(text=trs['back'][language])])
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

def generate_city_buttons(language: str, region: str):
    city_button = [[]]
    count = 0
    for i in city_data[language][region]:
        if count % 2 == 0:
                city_button[-1].append(KeyboardButton(text=i))
                count += 1
        else:
                city_button.append([KeyboardButton(text=i)])
                count = 0
    city_button.append([KeyboardButton(text=trs['back'][language])])
    keyboard = ReplyKeyboardMarkup(keyboard=city_button, resize_keyboard=True, one_time_keyboard=True)
    return keyboard    

def settings_buttons(language: str):
    buttons = [
                [KeyboardButton(text=trs['settings'][language][0]), KeyboardButton(text=trs['settings'][language][1])]]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return keyboard
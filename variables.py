from environs import Env
from json_actions import *

env = Env()
env.read_env()

TOKEN = env("BOT_TOKEN")

user_data = load_data("Json/user_info.json")
city_data = load_data("Json/city_info.json")
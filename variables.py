from environs import Env
from json_actions import *

env = Env()
env.read_env()

TOKEN = env("BOT_TOKEN")
GEMENI_KEY = env('GEMENI_API_KEY')

city_data = load_data("Json/city_info.json")
trs = load_data("Json/translation.json")

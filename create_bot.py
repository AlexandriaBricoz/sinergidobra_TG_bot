from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())

storage = MemoryStorage()

with open('config.json', 'r') as file:
    config_data = json.load(file)

master_id = config_data['master_id_owner']
bot_address =  config_data['bot_name']
bot = Bot(token=config_data["Token"])
dp = Dispatcher(bot, storage=storage)



client_commands = ['/start', '/help', 'Супер', 'Тренировки', 'Режим работы',\
    'Контакты', '/moderate']

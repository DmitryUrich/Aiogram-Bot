from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

API_TOKEN = 'your token'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
    

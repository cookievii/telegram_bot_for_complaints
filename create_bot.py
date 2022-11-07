import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

# Загрузка Секретных Ключей
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

bot = Bot(token=os.getenv("TOKEN_TELEGRAM"))
dp = Dispatcher(bot, storage=MemoryStorage())

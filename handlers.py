from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from models import async_session, User, Folder, init_db
from disk.py import YandexDisk
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
YANDEX_CLIENT_ID = os.getenv('YANDEX_CLIENT_ID')
YANDEX_CLIENT_SECRET = os.getenv('YANDEX_CLIENT_SECRET')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.reply("Привет! Ты хочешь зарегистрироваться как преподаватель или слушатель?")

@dp.message_handler(commands=['status'])
async def cmd_status(message: types.Message):
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if user:
            if user.yandex_token:
                await message.reply(f"Ты зарегистрирован в API Яндекс.Диска с токеном: {user.yandex_token}")
            else:
                await message.reply("Ты не зарегистрирован в API Яндекс.Диска. Используй команду /register для регистрации.")
        else:
            await message.reply("Ты не зарегистрирован. Используй команду /start для регистрации.")

@dp.message_handler(commands=['register'])
async def cmd_register(message: types.Message):
    await message.reply("Для регистрации в API Яндекс.Диска, перейди по ссылке и следуй инструкциям: <ссылка>")

@dp.message_handler(commands=['token'])
async def cmd_token(message: types.Message):
    token = message.text.split(' ')[1]
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if user:
            user.yandex_token = token
            await session.commit()
            await message.reply("Токен успешно сохранен!")
        else:
            await message.reply("Сначала зарегистрируйся с помощью команды /start")

@dp.message_handler(commands=['add'])
async def cmd_add(message: types.Message):
    folder_path = message.text.split(' ')[1]
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if user:
            folder = Folder(user_id=user.id, path=folder_path)
            session.add(folder)
            await session.commit()
            await message.reply("Папка успешно добавлена в отслеживаемые!")
        else:
            await message.reply("Сначала зарегистрируйся с помощью команды /start")

@dp.message_handler(commands=['delete'])
async def cmd_delete(message: types.Message):
    folder_path = message.text.split(' ')[1]
    async with async_session() as session:
        user = await session.get(User, message.from_user.id)
        if user:
            folder = await session.query(Folder).filter(Folder.user_id == user.id, Folder.path == folder_path).first()
            if folder:
                await session.delete(folder)
                await session.commit()
                await message.reply("Папка успешно удалена из отслеживаемых!")
            else:
                await message.reply("Папка не найдена!")
        else:
            await message.reply("Сначала зарегистрируйся с помощью команды /start")

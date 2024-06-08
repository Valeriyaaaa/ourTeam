from aiogram import executor
from handlers import dp
from models import init_db

async def on_startup(dispatcher):
    await init_db()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)

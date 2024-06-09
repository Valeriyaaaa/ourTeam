from aiogram import executor
from handlers import dp
from models import init_db
from aiohttp import web
import os

async def on_startup(dispatcher):
    await init_db()

async def handle(request):
    return web.Response(text="Bot is running")

def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    port = int(os.getenv('PORT', 8080))
    web.run_app(app, port=port)

if __name__ == "__main__":
    # Запускаем бота и веб-сервер параллельно
    from multiprocessing import Process

    bot_process = Process(target=executor.start_polling, args=(dp,), kwargs={'on_startup': on_startup})
    bot_process.start()

    web_server_process = Process(target=start_web_server)
    web_server_process.start()

    bot_process.join()
    web_server_process.join()

import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# Твій токен
TOKEN = "8996022290:AAHN8UffPwXENDVbHEUrxOyJX_kUdC5v7F0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Тестова команда /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("🔥 **Бот успішно запущений на Render!**\nЗв'язок 100%, працюємо 24/7 без лагів.", parse_mode="Markdown")

# --- МІКРО-СЕРВЕР ДЛЯ РЕНДЕРУ (ЩОБ НЕ ВИБИВАЛО ПОМИЛКУ ПОРТУ) ---
async def handle_ping(request):
    return web.Response(text="Bot is alive and running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Веб-сервер запущено на порту {port}")

# Головний запуск
async def main():
    await start_web_server()
    print("Запускаємо Telegram-бота...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

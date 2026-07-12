import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# 1. Твій новий токен від BotFather
TOKEN = "8996022290:AAEfKn0Tf3Qrqq0jbKd8KPizbPPeF2SfTAE"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопка капчі (перше повідомлення, яке прийде в лічку при подачі заявки)
captcha_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ ПОДТВЕРДИТЬ, ЧТО Я ЧЕЛОВЕК", callback_data="approve_user")]
])

# Кнопка з бонусом (друге повідомлення, після того як людина підтвердила капчу)
bonus_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💰 ЗАБРАТЬ БОНУС НА ДЕПОЗИТ", url="ТВІЙ_ЛІНК_НА_КАЗІК")]
])

# ГОЛОВНА ФУНКЦІЯ: Ловимо заявку на вступ у канал
@dp.chat_join_request()
async def handle_join_request(update: types.ChatJoinRequest):
    try:
        # Шлемо людині повідомлення в особисті повідомлення
        await bot.send_message(
            chat_id=update.from_user.id,
            text=f"⚠️ **Ваша заявка в канал «ЖЕСТКИЙ ПОЦ» на рассмотрении!**\n\n"
                 f"Чтобы получить доступ к материалам и активировать свой приветственный бонус, "
                 f"подтвердите, что вы живой человек и не являетесь ботом. Нажмите кнопку ниже:",
            reply_markup=captcha_kb,
            parse_mode="Markdown"
        )
        print(f"Зловив заявку від користувача {update.from_user.id}, відправив капчу.")
    except Exception as e:
        print(f"Не вдалося написати користувачу: {e}")

# Функція, яка спрацьовує при натисканні на кнопку капчі
@dp.callback_query(F.data == "approve_user")
async def approve_callback(callback: types.CallbackQuery):
    try:
        # 1. Автоматично схвалюємо заявку в канал
        await bot.approve_chat_join_request(
            chat_id=callback.message.chat.id,  # Бот сам візьме ID чату
            user_id=callback.from_user.id
        )
        
        # 2. Міняємо перше повідомлення на текст із бонусом (і НІЯКОЇ реклами Bot-T!)
        await callback.message.edit_text(
            text="✅ **Доступ открыт! Заявка успешно одобрена.**\n\n"
                 "🎁 Ваш приветственный бонус на первый депозит уже начислен. Забирайте его по кнопке ниже и переходите в канал!",
            reply_markup=bonus_kb,
            parse_mode="Markdown"
        )
    except Exception as e:
        print(f"Помилка при схваленні заявки: {e}")

# --- АНТИ-СОН СЕРВЕР ДЛЯ RENDER ---
async def handle_ping(request):
    return web.Response(text="Bot is active")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

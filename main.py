import asyncio
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web

# =====================================================================
# 1. ТАКЕН ВЖЕ ВШИТИЙ (НІЧОГО НЕ МІНЯЙ ТУТ):
TOKEN = "8996022290:AAHN8UffPwXENDVbHEUrxOyJX_kUdC5v7F0"

# 2. СЮДИ ВСТАВ СВОЄ РЕАЛЬНЕ ПОСИЛАННЯ НА КАЗІК:
CASINO_LINK = "https://t.me/твоя_силка_на_казік"
# =====================================================================

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопка капчі (перше повідомлення в ЛС)
captcha_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ ПОДТВЕРДИТЬ, ЧТО Я ЧЕЛОВЕК", callback_data="approve_user")]
])

# Кнопка з бонусом (після підтвердження)
bonus_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="💰 ЗАБРАТЬ БОНУС НА ДЕПОЗИТ", url=CASINO_LINK)]
])

# ЛОВИМО ЗАЯВКУ В КАНАЛ
@dp.chat_join_request()
async def handle_join_request(update: types.ChatJoinRequest):
    try:
        await bot.send_message(
            chat_id=update.from_user.id,
            text="⚠️ **Ваша заявка в канал «ЖЕСТКИЙ ПОЦ» на рассмотрении!**\n\n"
                 "Чтобы получить доступ к материалам и активировать свой приветственный бонус, "
                 "подтвердите, что вы живой человек и не являетесь ботом. Нажмите кнопку ниже:",
            reply_markup=captcha_kb,
            parse_mode="Markdown"
        )
        print(f" + Відправив капчу користувачу: {update.from_user.id}")
    except Exception as e:
        print(f" - Помилка відправки в ЛС: {e}")

# КОЛИ НАТИСНУЛИ КНОПКУ «ПОДТВЕРДИТЬ»
@dp.callback_query(F.data == "approve_user")
async def approve_callback(callback: types.CallbackQuery):
    try:
        # 1. Приймаємо людину в канал
        await bot.approve_chat_join_request(
            chat_id=callback.message.chat.id,
            user_id=callback.from_user.id
        )
        
        # 2. Даємо бонус без жодної реклами
        await callback.message.edit_text(
            text="✅ **Доступ открыт! Заявка успешно одобрена.**\n\n"
                 "🎁 Ваш приветственный бонус на первый депозит уже начислен. Забирайте его по кнопке ниже и переходите в канал!",
            reply_markup=bonus_kb,
            parse_mode="Markdown"
        )
        print(f" + Заявку схвалено для: {callback.from_user.id}")
    except Exception as e:
        print(f" - Помилка апруву: {e}")

# --- МІКРО-СЕРВЕР, ЩОБ РЕНДЕР НЕ ЗАСИНАВ І НЕ ВИДАВАВ ПОМИЛКУ ---
async def handle_ping(request):
    return web.Response(text="Bot is alive and working 24/7!")

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
    # Автоматично вбиваємо всі старі прив'язки до Bot-T при запуску:
    await bot.delete_webhook(drop_pending_updates=True)
    print(" === БОТ УСПІШНО ЗАПУЩЕНИЙ І ГОТОВИЙ РОЗЙОБУВАТИ ТРАФІК === ")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

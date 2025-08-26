import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datetime import datetime
import pytz
from aiogram.client.default import DefaultBotProperties

API_TOKEN = os.getenv("API_TOKEN")
GROUP_ID = -1003040890528   # guruh ID sini shu yerga yozasiz


bot = Bot(
    token=API_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Xabarlar sonini saqlash uchun lug‘at
user_messages = {}

# Har bir foydalanuvchi yozganini sanash
@dp.message()
async def count_messages(message: Message):
    if message.chat.id == GROUP_ID and message.from_user:
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.full_name
        user_messages[user_id] = {
            "username": username,
            "count": user_messages.get(user_id, {}).get("count", 0) + 1
        }

# Har kuni soat 20:00 da TOP 3 ni yuborish
async def send_daily_top():
    while True:
        now = datetime.now(pytz.timezone("Asia/Tashkent"))
        if now.hour == 20 and now.minute == 0:
            if user_messages:
                sorted_users = sorted(user_messages.items(), key=lambda x: x[1]["count"], reverse=True)[:3]
                text = "🎉 Bugungi TOP 3 faol ishtirokchilar:\n\n"
                for i, (uid, data) in enumerate(sorted_users, start=1):
                    text += f"{i}. {data['username']} – {data['count']} ta xabar\n"
                await bot.send_message(GROUP_ID, text)
                user_messages.clear()  # ertasi kun uchun hisobni tozalash
            await asyncio.sleep(60)  # shu minut ichida qayta yubormaslik uchun
        await asyncio.sleep(30)

async def main():
    asyncio.create_task(send_daily_top())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

#from src.handlers.welcome import router as welcome_router
from src.handlers.animal_quiz import router as quiz_router


load_dotenv()

BOT_TOKEN = os.getenv("TOKEN")

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден! Проверьте файл .env")

# Инициализация бота и диспетчера
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

#dp.include_router(welcome_router)
dp.include_router(quiz_router)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

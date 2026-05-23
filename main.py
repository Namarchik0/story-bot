import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import TOKEN
from handlers.user import router as user_router
from handlers.admin import router as admin_router
from database import create_db

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(admin_router)


async def main():

    logging.basicConfig(level=logging.INFO)

    await create_db()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
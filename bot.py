from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN, ADMIN_IDS
from database import *

import asyncio

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()

# Временное хранение данных
user_data = {}

@dp.message(Command("start"))
async def start(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Читать рассказы", callback_data="stories")]
        ]
    )

    await message.answer(
        "📖 <b>Добро пожаловать в библиотеку рассказов</b>",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "stories")
async def stories_list(callback: CallbackQuery):
    stories = await get_stories()

    buttons = []

    for story in stories:
        buttons.append([
            InlineKeyboardButton(
                text=f"📖 {story[1]}",
                callback_data=f"story_{story[0]}"
            )
        ])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.answer(
        "📚 <b>Список рассказов:</b>",
        reply_markup=keyboard
    )

    await callback.answer()

@dp.callback_query(F.data.startswith("edit_"))
async def edit_story(callback: CallbackQuery):

    if callback.from_user.id not in ADMIN_IDS:
        await callback.answer(
            "⛔ Нет доступа",
            show_alert=True
        )
        return

    story_id = int(callback.data.split("_")[1])

    editing_story[callback.from_user.id] = story_id

    await callback.message.answer(
        "✏ Отправьте новый текст рассказа:"
    )

    await callback.answer()
async def open_story(callback: CallbackQuery):
    story_id = int(callback.data.split("_")[1])

    story = await get_story(story_id)

    if not story:
        return

    text = f"""
<b>{story[1]}</b>

{story[2]}
"""

    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="⬅ Назад",
                callback_data="stories"
            )
        ],
        [
            InlineKeyboardButton(
                text="🏠 Главное меню",
                callback_data="menu"
            )
        ]
    ]
)

    await callback.message.delete()

    await bot.send_photo(
        callback.from_user.id,
        photo=story[3],
        caption=text,
        reply_markup=keyboard
    )

@dp.message(Command("add"))
async def add_story_start(message: Message):

    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет доступа")
        return

    user_data[message.from_user.id] = {}

    await message.answer("✍ Введите название рассказа:")
    user_data[message.from_user.id] = {}

    await message.answer("✍ Введите название рассказа:")

@dp.message()
async def process_add(message: Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        return

    data = user_data[user_id]

    if "title" not in data:
        data["title"] = message.text
        await message.answer("📄 Теперь отправьте текст рассказа:")
        return

    if "text" not in data:
        data["text"] = message.text
        await message.answer("🖼 Теперь отправьте картинку:")
        return

    if message.photo:
        photo_id = message.photo[-1].file_id

        await add_story(
            data["title"],
            data["text"],
            photo_id
        )

        del user_data[user_id]

        await message.answer("✅ Рассказ добавлен!")

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
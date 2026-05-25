import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from config import TOKEN, ADMINS
from keyboards import (
    main_menu,
    admin_menu,
    back_menu,
    cancel_menu
)

from database import *
from states import (
    AddStory,
    EditStory
)

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

dp = Dispatcher()

# =========================
# START
# =========================

@dp.message(CommandStart())
async def start(message: Message):

    if message.from_user.id in ADMINS:

        await message.answer(
            "👋 Админ панель",
            reply_markup=admin_menu()
        )

    else:

        await message.answer(
            "📚 Добро пожаловать!",
            reply_markup=main_menu()
        )

# =========================
# HOME
# =========================

@dp.callback_query(F.data == "home")
async def home(callback: CallbackQuery):

    await callback.message.delete()

    if callback.from_user.id in ADMINS:

        await callback.message.answer(
            "🏠 Главное меню",
            reply_markup=admin_menu()
        )

    else:

        await callback.message.answer(
            "🏠 Главное меню",
            reply_markup=main_menu()
        )

# =========================
# STORIES
# =========================

@dp.callback_query(F.data == "stories")
async def stories(callback: CallbackQuery):

    await callback.message.delete()

    stories_list = await get_stories()

    buttons = []

    for story in stories_list:

        buttons.append([
            InlineKeyboardButton(
                text=story[1],
                callback_data=f"story_{story[0]}"
            )
        ])

    buttons.append([
        InlineKeyboardButton(
            text="🏠 Главное меню",
            callback_data="home"
        )
    ])

    kb = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.answer(
        "📚 Список рассказов",
        reply_markup=kb
    )

# =========================
# OPEN STORY
# =========================

@dp.callback_query(F.data.startswith("story_"))
async def open_story(callback: CallbackQuery):

    await callback.message.delete()

    story_id = int(callback.data.split("_")[1])

    story = await get_story(story_id)

    title = story[1]
    text = story[2]
    photo = story[3]

    kb = InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="⭐1",
                    callback_data=f"rate_{story_id}_1"
                ),

                InlineKeyboardButton(
                    text="⭐2",
                    callback_data=f"rate_{story_id}_2"
                ),

                InlineKeyboardButton(
                    text="⭐3",
                    callback_data=f"rate_{story_id}_3"
                ),

                InlineKeyboardButton(
                    text="⭐4",
                    callback_data=f"rate_{story_id}_4"
                ),

                InlineKeyboardButton(
                    text="⭐5",
                    callback_data=f"rate_{story_id}_5"
                ),
            ],

            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="stories"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="home"
                )
            ]
        ]
    )

    if photo:

        await callback.message.answer_photo(
            photo=photo,
            caption=f"<b>{title}</b>\n\n{text}",
            reply_markup=kb
        )

    else:

        await callback.message.answer(
            f"<b>{title}</b>\n\n{text}",
            reply_markup=kb
        )

# =========================
# RATE
# =========================

@dp.callback_query(F.data.startswith("rate_"))
async def rate(callback: CallbackQuery):

    data = callback.data.split("_")

    story_id = int(data[1])
    rating = int(data[2])

    await add_rating(
        callback.from_user.id,
        story_id,
        rating
    )

    await callback.answer(
        f"Вы поставили {rating} ⭐"
    )

# =========================
# ADD STORY
# =========================

@dp.callback_query(F.data == "add_story")
async def add_story_start(
        callback: CallbackQuery,
        state: FSMContext
):

    await callback.message.delete()

    await state.set_state(AddStory.title)

    await callback.message.answer(
        "✏ Введите название:"
    )

@dp.message(AddStory.title)
async def add_title(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        title=message.text
    )

    await state.set_state(AddStory.text)

    await message.answer(
        "📖 Отправьте текст:"
    )

@dp.message(AddStory.text)
async def add_text(
        message: Message,
        state: FSMContext
):

    await state.update_data(
        text=message.text
    )

    await state.set_state(AddStory.photo)

    await message.answer(
        "🖼 Отправьте фото:"
    )

@dp.message(AddStory.photo)
async def add_photo(
        message: Message,
        state: FSMContext
):

    data = await state.get_data()

    photo = None

    if message.photo:
        photo = message.photo[-1].file_id

    await add_story(
        data["title"],
        data["text"],
        photo
    )

    await state.clear()

    await message.answer(
        "✅ Рассказ добавлен!",
        reply_markup=admin_menu()
    )

# =========================
# DELETE STORY
# =========================

@dp.callback_query(F.data == "delete_story")
async def delete_story_menu(
        callback: CallbackQuery
):

    await callback.message.delete()

    stories_list = await get_stories()

    buttons = []

    for story in stories_list:

        buttons.append([
            InlineKeyboardButton(
                text=f"🗑 {story[1]}",
                callback_data=f"delete_{story[0]}"
            )
        ])

    kb = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.answer(
        "🗑 Выберите рассказ",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("delete_"))
async def delete_story_confirm(
        callback: CallbackQuery
):

    story_id = int(
        callback.data.split("_")[1]
    )

    await delete_story(story_id)

    await callback.message.delete()

    await callback.message.answer(
        "✅ Удалено",
        reply_markup=admin_menu()
    )

# =========================
# EDIT STORY
# =========================

story_edit_id = {}

@dp.callback_query(F.data == "edit_story")
async def edit_story_menu(
        callback: CallbackQuery
):

    await callback.message.delete()

    stories_list = await get_stories()

    buttons = []

    for story in stories_list:

        buttons.append([
            InlineKeyboardButton(
                text=f"✏ {story[1]}",
                callback_data=f"edit_{story[0]}"
            )
        ])

    kb = InlineKeyboardMarkup(
        inline_keyboard=buttons
    )

    await callback.message.answer(
        "✏ Выберите рассказ",
        reply_markup=kb
    )

@dp.callback_query(F.data.startswith("edit_"))
async def edit_story_start(
        callback: CallbackQuery,
        state: FSMContext
):

    story_id = int(
        callback.data.split("_")[1]
    )

    story = await get_story(story_id)

    title = story[1]
    text = story[2]

    story_edit_id[
        callback.from_user.id
    ] = story_id

    await state.set_state(
        EditStory.text
    )

    await callback.message.delete()

    await callback.message.answer(

    f"✏ <b>Редактирование рассказа:</b>\n\n"
    f"📚 <b>{title}</b>\n\n"
    f"{text}\n\n"

    f"——————————————\n"
    f"Отправьте НОВЫЙ текст рассказа:",

    reply_markup=cancel_menu()
)
    
@dp.message(EditStory.text)
async def edit_story_save(
        message: Message,
        state: FSMContext
):

    story_id = story_edit_id[
        message.from_user.id
    ]

    await update_story(
        story_id,
        message.text
    )

    await state.clear()

    await message.answer(
        "✅ Рассказ обновлен",
        reply_markup=admin_menu()
    )

# =========================
# START BOT
# =========================

@dp.callback_query(F.data == "cancel_edit")
async def cancel_edit(
        callback: CallbackQuery,
        state: FSMContext
):

    await state.clear()

    await callback.message.delete()

    await callback.message.answer(
        "❌ Редактирование отменено",
        reply_markup=admin_menu()
    )
    
async def main():

    await db_start()

    await bot.delete_webhook(
        drop_pending_updates=True
    )

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
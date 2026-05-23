from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database import get_stories, get_story
from keyboards import (
    menu_keyboard,
    story_keyboard,
    admin_keyboard
)
from config import ADMINS

router = Router()


@router.message(Command("start"))
async def start(message: Message):

    stories = await get_stories()

    if message.from_user.id in ADMINS:

        await message.answer(
            "👑 Админ панель",
            reply_markup=admin_keyboard()
        )

    await message.answer(
        "📚 Выберите рассказ",
        reply_markup=menu_keyboard(stories)
    )


@router.callback_query(F.data.startswith("story_"))
async def open_story(callback: CallbackQuery):

    story_id = callback.data.split("_")[1]

    story = await get_story(story_id)

    if story[3]:

        await callback.message.answer_photo(
            photo=story[3],
            caption=f"<b>{story[1]}</b>\n\n{story[2]}",
            reply_markup=story_keyboard()
        )

    else:

        await callback.message.answer(
            f"<b>{story[1]}</b>\n\n{story[2]}",
            reply_markup=story_keyboard()
        )

    await callback.answer()


@router.callback_query(F.data == "menu")
@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):

    stories = await get_stories()

    await callback.message.answer(
        "📚 Меню рассказов",
        reply_markup=menu_keyboard(stories)
    )

    await callback.answer()
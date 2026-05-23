from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import ADMINS
from database import add_story, get_stories
from keyboards import menu_keyboard

router = Router()

states = {}


@router.callback_query(F.data == "add_story")
async def add_story_start(callback: CallbackQuery):

    if callback.from_user.id not in ADMINS:
        return

    states[callback.from_user.id] = {}

    states[callback.from_user.id]["step"] = "title"

    await callback.message.answer(
        "Введите название рассказа"
    )

    await callback.answer()


@router.message()
async def add_story_process(message: Message):

    if message.from_user.id not in ADMINS:
        return

    if message.from_user.id not in states:
        return

    state = states[message.from_user.id]

    if state["step"] == "title":

        state["title"] = message.text
        state["step"] = "text"

        await message.answer(
            "Введите текст"
        )

    elif state["step"] == "text":

        state["text"] = message.text
        state["step"] = "photo"

        await message.answer(
            "Отправьте фото или напишите skip"
        )

    elif state["step"] == "photo":

        photo = None

        if message.photo:
            photo = message.photo[-1].file_id

        await add_story(
            state["title"],
            state["text"],
            photo
        )

        stories = await get_stories()

        await message.answer(
            "✅ Рассказ добавлен",
            reply_markup=menu_keyboard(stories)
        )

        del states[message.from_user.id]
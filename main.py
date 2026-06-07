import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, ADMINS
from database import (
    init_db,
    add_story,
    get_stories,
    get_story,
    delete_story,
    update_story,
    add_rating,
    get_rating
)
from keyboards import main_menu, finish_kb, rating_kb
from states import AddStory, EditStory

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


def is_admin(user_id: int):
    return user_id in ADMINS


# ---------------- START ----------------

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "📚 Главное меню",
        reply_markup=main_menu(is_admin(message.from_user.id))
    )


@router.callback_query(F.data == "home")
async def home(c: CallbackQuery):
    await c.message.edit_text(
        "📚 Главное меню",
        reply_markup=main_menu(is_admin(c.from_user.id))
    )
    await c.answer()


# ---------------- READ ----------------

@router.callback_query(F.data == "read")
async def read(c: CallbackQuery):
    stories = await get_stories()

    kb = []
    for s in stories:
        kb.append([
            InlineKeyboardButton(
                text=s[1],
                callback_data=f"story_{s[0]}"
            )
        ])

    await c.message.edit_text(
        "Выбери рассказ:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )
    await c.answer()


@router.callback_query(F.data.startswith("story_"))
async def story(c: CallbackQuery):
    story_id = int(c.data.split("_")[1])

    s = await get_story(story_id)
    avg, count = await get_rating(story_id)

    # убираем меню выбора рассказов
    await c.message.delete()

    title = f"<b>{s[1]}</b>\n\n"
    content = s[2]

    limit = 4000

    for i in range(0, len(content), limit):
        part = content[i:i + limit]

        if i == 0:
            await c.message.answer(
                title + part,
                parse_mode="HTML"
            )
        else:
            await c.message.answer(part)

    await c.message.answer(
        f"⭐ {round(avg or 0,1)} ({count})",
        reply_markup=rating_kb(story_id)
    )

    await c.answer()


@router.callback_query(F.data.startswith("rate_"))
async def rate(c: CallbackQuery):
    _, sid, r = c.data.split("_")

    await add_rating(int(sid), c.from_user.id, int(r))
    await c.answer("Оценено!")


# ---------------- ADD STORY ----------------

@router.callback_query(F.data == "add")
async def add(c: CallbackQuery, state: FSMContext):
    if not is_admin(c.from_user.id):
        return await c.answer("Нет доступа")

    await state.set_state(AddStory.title)
    await c.message.edit_text("Введите название:")
    await c.answer()


@router.message(AddStory.title)
async def title(m: Message, state: FSMContext):

    await state.update_data(title=m.text, parts=[])

    await state.set_state(AddStory.content)

    await m.answer(
        "Пиши текст. Когда закончишь — нажми Готово или Назад",
        reply_markup=finish_kb()
    )


@router.message(AddStory.content, F.text != "✅ Готово")
async def collect(m: Message, state: FSMContext):
    data = await state.get_data()
    parts = data["parts"]
    parts.append(m.text)
    await state.update_data(parts=parts)

@router.message(AddStory.title, F.text == "⬅️ Назад")
async def cancel_title(m: Message, state: FSMContext):

    await state.clear()

    await m.answer("❌ Добавление отменено")

    await m.answer(
        "📚 Главное меню",
        reply_markup=main_menu(
            is_admin(m.from_user.id)
        )
    )

@router.message(AddStory.content, F.text == "⬅️ Назад")
async def cancel_add(m: Message, state: FSMContext):

    await state.clear()

    await m.answer(
        "❌ Добавление отменено",
        reply_markup=ReplyKeyboardRemove()
    )

    await m.answer(
        "📚 Главное меню",
        reply_markup=main_menu(
            is_admin(m.from_user.id)
        )
    )


@router.message(AddStory.content, F.text == "✅ Готово")
async def save(m: Message, state: FSMContext):
    data = await state.get_data()

    await add_story(
        data["title"],
        "\n\n".join(data["parts"])
    )

    await state.clear()

    # 🔥 УБИРАЕМ КНОПКУ "ГОТОВО"
    await m.answer(
        "✅ Сохранено",
        reply_markup=ReplyKeyboardRemove()
    )

    # возвращаем меню
    await m.answer(
        "📚 Меню",
        reply_markup=main_menu(is_admin(m.from_user.id))
    )

@router.callback_query(F.data == "edit")
async def edit_menu(c: CallbackQuery):

    if not is_admin(c.from_user.id):
        return await c.answer("Нет доступа")

    stories = await get_stories()

    kb = []

    for s in stories:
        kb.append([
            InlineKeyboardButton(
                text=s[1],
                callback_data=f"edit_{s[0]}"
            )
        ])

    await c.message.edit_text(
        "Выбери рассказ:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )

    await c.answer()

@router.callback_query(F.data.startswith("edit_"))
async def edit_story(c: CallbackQuery, state: FSMContext):

    story_id = int(c.data.split("_")[1])

    story = await get_story(story_id)

    await state.update_data(story_id=story_id)

    await state.set_state(EditStory.content)

    await c.message.answer(
        f"Текущий текст:\n\n{story[2]}\n\nОтправь новую версию текста."
    )

    await c.answer()

@router.message(EditStory.content)
async def save_edit(m: Message, state: FSMContext):

    data = await state.get_data()

    await update_story(
        data["story_id"],
        m.text
    )

    await state.clear()

    await m.answer(
        "✅ Рассказ обновлён",
        reply_markup=main_menu(
            is_admin(m.from_user.id)
        )
    )


# ---------------- DELETE ----------------

@router.callback_query(F.data == "delete")
async def delete_menu(c: CallbackQuery):

    if not is_admin(c.from_user.id):
        return await c.answer("Нет доступа")

    stories = await get_stories()

    if not stories:
        await c.message.edit_text("Нет рассказов")
        return await c.answer()

    kb = []
    for s in stories:
        kb.append([
            InlineKeyboardButton(
                text=s[1],
                callback_data=f"del_{s[0]}"
            )
        ])

    await c.message.edit_text(
        "Выбери рассказ для удаления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=kb)
    )
    await c.answer()


@router.callback_query(F.data.startswith("del_"))
async def do_delete(c: CallbackQuery):
    story_id = int(c.data.split("_")[1])

    await delete_story(story_id)

    await c.message.edit_text(
        "✅ Удалено"
    )

    await c.message.answer(
        "📚 Главное меню",
        reply_markup=main_menu(
            is_admin(c.from_user.id)
        )
    )

    await c.answer()


# ---------------- MAIN ----------------

async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
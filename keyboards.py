from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import AUTHOR_LINK


def main_menu(is_admin=False):
    kb = [
        [InlineKeyboardButton(text="📖 Читать", callback_data="read")],
    ]

    if is_admin:
        kb.append([InlineKeyboardButton(text="➕ Добавить", callback_data="add")])
        kb.append([InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit")])
        kb.append([InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")])

    kb.append([InlineKeyboardButton(text="👤 Автор", url=AUTHOR_LINK)])

    return InlineKeyboardMarkup(inline_keyboard=kb)


def finish_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Готово")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )


def rating_kb(story_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐1", callback_data=f"rate_{story_id}_1"),
            InlineKeyboardButton(text="⭐2", callback_data=f"rate_{story_id}_2"),
            InlineKeyboardButton(text="⭐3", callback_data=f"rate_{story_id}_3"),
            InlineKeyboardButton(text="⭐4", callback_data=f"rate_{story_id}_4"),
            InlineKeyboardButton(text="⭐5", callback_data=f"rate_{story_id}_5"),
        ],
        [InlineKeyboardButton(text="🏠 Меню", callback_data="home")]
    ])
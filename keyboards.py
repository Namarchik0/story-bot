from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu(is_admin=False):
    buttons = [
        [InlineKeyboardButton(text="📖 Читать рассказы", callback_data="stories")],
        [InlineKeyboardButton(text="👤 Автор", url="https://t.me/Luntik_kss")]
    ]

    if is_admin:
        buttons.insert(
            1,
            [InlineKeyboardButton(text="➕ Добавить рассказ", callback_data="add_story")]
        )

        buttons.insert(
            2,
            [InlineKeyboardButton(text="✏️ Редактировать", callback_data="edit_story")]
        )

        buttons.insert(
            3,
            [InlineKeyboardButton(text="🗑 Удалить", callback_data="delete_story")]
        )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
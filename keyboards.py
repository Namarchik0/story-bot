from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import SUPPORT_LINK, AUTHOR_LINK


def main_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 Читать рассказы",
                    callback_data="stories"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🆘 Поддержка",
                    url=SUPPORT_LINK
                ),
                InlineKeyboardButton(
                    text="👨‍💻 Автор",
                    url=AUTHOR_LINK
                )
            ]
        ]
    )


def admin_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[

            [
                InlineKeyboardButton(
                    text="📚 Читать рассказы",
                    callback_data="stories"
                )
            ],

            [
                InlineKeyboardButton(
                    text="➕ Добавить",
                    callback_data="add_story"
                )
            ],

            [
                InlineKeyboardButton(
                    text="✏ Редактировать",
                    callback_data="edit_story"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data="delete_story"
                )
            ],

            [
                InlineKeyboardButton(
                    text="🆘 Поддержка",
                    url=SUPPORT_LINK
                ),

                InlineKeyboardButton(
                    text="👨‍💻 Автор",
                    url=AUTHOR_LINK
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


def back_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ Назад",
                    callback_data="stories"
                ),
                InlineKeyboardButton(
                    text="🏠 Главное меню",
                    callback_data="home"
                )
            ]
        ]
    )
def cancel_menu():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅ Отмена",
                    callback_data="cancel_edit"
                )
            ]
        ]
    )
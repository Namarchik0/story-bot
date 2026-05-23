from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
def bottom_menu():

    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🏠 Главное меню"
                )
            ]
        ],
        resize_keyboard=True
    )


def menu_keyboard(stories):

    buttons = []

    for story in stories:

        buttons.append([
            InlineKeyboardButton(
                text=story[1],
                callback_data=f"story_{story[0]}"
            )
        ])

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def story_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back"
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


def admin_keyboard():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➕ Добавить рассказ",
                    callback_data="add_story"
                )
            ]
        ]
    )
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Список сессий", callback_data="show_all_sessions")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def sessions_list_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Создать сессию", callback_data="create_new_session")],
        [InlineKeyboardButton(text="Список сессий", callback_data="show_all_sessions")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def ready_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Готово", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def return_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def sessions_list_keyboard(sessions: list):
    buttons = []
    for session_id in sessions:
        buttons.append([InlineKeyboardButton(text=session_id, callback_data=f"session_{session_id}")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="main_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def session_keyboard(session_id: int):
    buttons = [
        [InlineKeyboardButton(text="Завершить", callback_data=f"stop_session_{session_id}")],
        [InlineKeyboardButton(text="Назад", callback_data="show_all_sessions")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def session_deleted_keyboard():
    buttons = [
        [InlineKeyboardButton(text="Готово", callback_data="show_all_sessions")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
import yaml

import keyboards

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

TOKEN = config["token"]
PASS = config["password"]

SESSIONS_URL = "http://127.0.0.1:8041"

router = Router()


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Привет!\n\n"
        "Этот бот создан специально для управления сервером презентаций виртуальной реальности\n\n"
        "Введи ключ доступа 👇"
    )


@router.message()
async def echo_handler(message: types.Message) -> None:
    try:
        message_body = message.text.split()

        if message_body[0] != PASS:
            await message.answer("<b>NULL!</b>")
        else:
            await message.answer(
                "Меню",
                reply_markup=keyboards.main_keyboard()
            )

    except TypeError:
        pass


@router.callback_query(Text("main_menu"))
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "Меню",
        reply_markup=keyboards.main_keyboard()
    )
    await callback.answer()


@router.callback_query(Text("show_all_sessions"))
async def show_all_sessions(callback: CallbackQuery):
    r = requests.get(url=SESSIONS_URL + "/session/all")
    if r.status_code == 200:
        sessions_list = r.json()
        if sessions_list:
            await callback.message.edit_text(
                "Sessions: ",
                reply_markup=keyboards.sessions_list_keyboard(sessions_list)
            )
            await callback.answer()
        else:
            await callback.message.edit_text(
                "No sessions created!",
                reply_markup=keyboards.return_keyboard()
            )


@router.callback_query(Text("create_new_session"))
async def create_new_session(callback: CallbackQuery):
    r = requests.get(url=SESSIONS_URL + "/session/new")
    if r.status_code == 201:
        await callback.message.edit_text(
            f"Session ID: {r.json()}",
            reply_markup=keyboards.ready_keyboard()
        )
        await callback.answer()


@router.callback_query(Text(startswith="stop_session_"))
async def stop_session(callback: CallbackQuery):
    session_id = callback.data.split("_")[-1]

    r = requests.delete(url=SESSIONS_URL + f"/session/{session_id}/stop")
    if r.status_code == 200:
        await callback.message.edit_text(
            f"Сессия завершена",
            reply_markup=keyboards.session_deleted_keyboard()
        )
        await callback.answer()
    elif r.status_code == 404:
        await callback.message.edit_text(
            f"Такой сессии не существует",
            reply_markup=keyboards.return_keyboard()
        )
        await callback.answer()


@router.callback_query(Text(startswith="session_"))
async def session_menu(callback: CallbackQuery):
    session_id = callback.data.split("_")[-1]

    await callback.message.edit_text(
        f"Session ID: {session_id}",
        reply_markup=keyboards.session_keyboard(session_id)
    )
    await callback.answer()


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    bot = Bot(TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

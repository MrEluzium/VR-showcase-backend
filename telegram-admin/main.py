import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
import yaml

import keyboards

with open("config.yaml") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

TOKEN = config["token"]
PASS = config["password"]

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
async def show_all_sessions(callback: CallbackQuery):
    await callback.message.edit_text(
        "Меню",
        reply_markup=keyboards.main_keyboard()
    )
    await callback.answer()


@router.callback_query(Text("show_all_sessions"))
async def show_all_sessions(callback: CallbackQuery):
    await callback.message.edit_text(
        "Sessions: ",
        reply_markup=keyboards.sessions_list_keyboard()
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

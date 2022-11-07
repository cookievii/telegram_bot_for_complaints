import os

from aiogram import Dispatcher, types
from aiogram.types import ParseMode

from core.messages import GREETING
from core.utils import check_status_user
from keyboards.start import KbStart


async def start(message: types.Message):
    """
    Проверяет на регистрацию пользователей:
        Если зарегистрирован - предоставляет главное меню;
        Если не зарегистрирован - направляет на форму регистрации.
    """
    user_status = await check_status_user(message)

    if user_status and user_status.banned is False:
        await message.answer(
            text=GREETING,
            reply_markup=KbStart().get_main(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")

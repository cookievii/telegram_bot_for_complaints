import os

from aiogram import Dispatcher, types
from aiogram.types import ParseMode

from core.messages import GREETING
from handlers.user import create_user
from keyboards.start import KbStart
from models.user import User


async def start(message: types.Message):
    """
    Проверяет на регистрацию пользователей:
        Если зарегистрирован - предоставляет главное меню;
        Если не зарегистрирован - направляет на форму регистрации.
    """
    if message.chat.id == os.getenv('ADMIN_GROUP'):
        test = message
        return

    is_registered = await User(user_id=message.from_user.id).exists()
    if is_registered:
        return await message.answer(
            text=GREETING,
            reply_markup=KbStart().get_main(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    await create_user(message)


def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")

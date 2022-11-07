import os
from typing import Optional

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

from core.messages import GREETING_ADMIN
from keyboards.admin import KbAdmin
from models.user import User

ADMIN_CHAT_ID = int(os.getenv("ADMIN_GROUP"))


async def check_status_user(message: types.Message):
    """
    Проверяет статус пользователя:
        - если админ - выдает админ панель;
        - если пользователь не прошел регистрацию - выдает форму регистрации;
        - если пользователь забанен - запрещает обращение к боту;
        - Иначе возвращает пользователя.
    """

    if message.chat.id == ADMIN_CHAT_ID:
        await message.answer(text=GREETING_ADMIN, reply_markup=KbAdmin().get_main())
        return False

    user: User = await User().search_user_by_any_arg(arg=message.chat.id)

    if user is None:
        from handlers.user import create_user

        await create_user(message)
        return False

    elif user.banned is True:
        await message.answer(
            text="Вам запретили обращаться к боту.", reply_markup=ReplyKeyboardRemove()
        )
        return False

    return user

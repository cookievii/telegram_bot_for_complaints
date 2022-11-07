from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from core.messages import (ASK_ANY_ARG_USER, ASK_ANY_ARG_USER_TO_PERMISSION,
                           ASK_MSG_TO_SPAM, BACK_TO_ADMIN_MENU, GREETING_ADMIN,
                           PERMISSION, SEARCH_USER, SPAM_MSG,
                           SUCCESSFUL_SEARCH_USER, SUCCESSFUL_SENT_MSG,
                           USER_NOT_FOUND)
from create_bot import bot
from keyboards.admin import KbAdmin
from models.user import User


class StepsAdmin(StatesGroup):
    search = State()
    permission = State()
    spam = State()


async def admin_start(message: types.Message):
    if message.text == SEARCH_USER:
        await StepsAdmin.search.set()
        await message.answer(text=ASK_ANY_ARG_USER, reply_markup=KbAdmin().get_back())

    elif message.text == PERMISSION:
        await StepsAdmin.permission.set()
        await message.answer(
            text=ASK_ANY_ARG_USER_TO_PERMISSION, reply_markup=KbAdmin().get_back()
        )

    elif message.text == SPAM_MSG:
        await StepsAdmin.spam.set()
        await message.answer(text=ASK_MSG_TO_SPAM, reply_markup=KbAdmin().get_back())


async def get_callback_back_to_main(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == BACK_TO_ADMIN_MENU:
        await state.finish()
        await callback.message.answer(
            text=GREETING_ADMIN, reply_markup=KbAdmin().get_main()
        )
        await callback.answer()


async def get_massage_search_user(message: types.Message):
    user = await User().search_user_by_any_arg(arg=message.text)
    if user is None:
        await message.answer(
            text=USER_NOT_FOUND,
            reply_markup=KbAdmin().get_back(),
            parse_mode=ParseMode.HTML,
        )

    else:
        await message.answer(
            text=SUCCESSFUL_SEARCH_USER.format(
                user_id=user.user_id,
                username=user.username,
                full_name=user.full_name,
                phone=user.phone,
                banned=user.banned,
            ),
            reply_markup=KbAdmin().get_back(),
            parse_mode=ParseMode.HTML,
        )


async def get_message_permission_user(message: types.Message):
    user = await User().search_user_by_any_arg(arg=message.text)
    if user is None:
        return await message.answer(
            text=USER_NOT_FOUND,
            reply_markup=KbAdmin().get_back(),
            parse_mode=ParseMode.HTML,
        )

    if user.banned:
        await User().unban_by_user_id(user_id=user.user_id)

    else:
        await User().ban_by_user_id(user_id=user.user_id)
    await message.answer(
        text=SUCCESSFUL_SEARCH_USER.format(
            user_id=user.user_id,
            username=user.username,
            full_name=user.full_name,
            phone=user.phone,
            banned=user.banned,
        ),
        reply_markup=KbAdmin().get_back(),
        parse_mode=ParseMode.HTML,
    )


async def get_message_spam(message: types.Message):
    users = await User().get_all()

    for user in users:
        await bot.send_message(chat_id=user.user_id, text=message.text)

    await message.reply(
        text=SUCCESSFUL_SENT_MSG,
        reply_markup=KbAdmin().get_back(),
    )


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, Text(equals=[SEARCH_USER, PERMISSION, SPAM_MSG])
    )
    dp.register_callback_query_handler(
        get_callback_back_to_main, state=StepsAdmin.search
    )
    dp.register_message_handler(get_massage_search_user, state=StepsAdmin.search)
    dp.register_callback_query_handler(
        get_callback_back_to_main, state=StepsAdmin.permission
    )
    dp.register_message_handler(
        get_message_permission_user, state=StepsAdmin.permission
    )
    dp.register_callback_query_handler(get_callback_back_to_main, state=StepsAdmin.spam)
    dp.register_message_handler(get_message_spam, state=StepsAdmin.spam)

import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ParseMode, ContentType

from core.messages import CONTACT, CHOOSE_COMMUNICATE, BACK, COMMUNICATE_ADMIN, CALL_ME, ASK_CORRECT_PHONE, YES, \
    INCORRECT_PHONE, DISPATCHER_WILL_CALL, MESSAGE_FOR_DISPATCHER, GREETING, SETTINGS_MESSAGE, \
    SUCCESS_CONNECT_WITH_ADMIN, CLOSE_CONNECT, CLOSED_CONNECT_WITH_ADMIN, MSG_FROM_USER
from create_bot import bot
from keyboards.communicate import KbCommunicate
from keyboards.start import KbStart
from keyboards.user import KbSetUser
from models.user import User

ADMIN_CHAT_ID = os.getenv("ADMIN_GROUP")


class StepSuccessfulPhone(StatesGroup):
    is_successful_phone = State()


class StepConnectWithAdmin(StatesGroup):
    connect = State()


async def start_communicate(message: types.Message):
    await message.answer(
        text=CHOOSE_COMMUNICATE,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=KbCommunicate.get_main())


async def get_callback_start(call: types.CallbackQuery):
    if call.data == CALL_ME:
        user = await User(user_id=call.from_user.id).get_by_id()
        text = ASK_CORRECT_PHONE.format(phone=user.phone)

        await StepSuccessfulPhone.is_successful_phone.set()
        await call.message.answer(
            text=text,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=KbCommunicate().get_check_phone_menu())

    elif call.data == COMMUNICATE_ADMIN:
        await StepConnectWithAdmin.connect.set()
        await call.message.answer(
            text=SUCCESS_CONNECT_WITH_ADMIN,
            parse_mode=ParseMode.HTML,
            reply_markup=KbCommunicate().get_close_connect()
        )

    elif call.data == BACK:
        await call.message.answer(
            text=GREETING,
            reply_markup=KbStart().get_main(),
            parse_mode=ParseMode.MARKDOWN_V2
        )
    await call.answer()


async def is_successful_phone(call: types.CallbackQuery, state: FSMContext):
    if call.data == YES:
        user = await User(user_id=call.from_user.id).get_by_id()
        text = MESSAGE_FOR_DISPATCHER.format(
            tg_username=call.message.from_user.username,
            full_name=user.full_name,
            phone=user.phone
        )
        await state.finish()
        await bot.send_message(chat_id=ADMIN_CHAT_ID, text=text, parse_mode=ParseMode.HTML)
        await call.message.answer(text=DISPATCHER_WILL_CALL, parse_mode=ParseMode.MARKDOWN_V2,
                                  reply_markup=KbStart().get_main())
    elif call.data == INCORRECT_PHONE:
        await state.finish()
        await call.message.answer(
            text=SETTINGS_MESSAGE,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=KbSetUser().get_main())
    await call.answer()


async def connect_with_admin(call: types.CallbackQuery, state: FSMContext):
    if call.data == CLOSE_CONNECT:
        await state.finish()
        await call.message.answer(
            text=CLOSED_CONNECT_WITH_ADMIN,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=KbStart().get_main())
    await call.answer()


async def message_to_admin(message: types.Message):
    user = await User(user_id=message.from_user.id).get_by_id()
    await bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=MSG_FROM_USER.format(
            tg_username=message.from_user.username,
            full_name=user.full_name,
            massage=message.text
        ),
        parse_mode=ParseMode.HTML
    )


def register_handlers_contact(dp: Dispatcher):
    dp.register_message_handler(start_communicate, Text(equals=CONTACT))
    dp.register_callback_query_handler(get_callback_start, Text(equals=[CALL_ME, COMMUNICATE_ADMIN, BACK]))
    dp.register_callback_query_handler(is_successful_phone, state=StepSuccessfulPhone.is_successful_phone)
    dp.register_callback_query_handler(connect_with_admin, state=StepConnectWithAdmin.connect)
    dp.register_message_handler(message_to_admin, content_types=ContentType.TEXT, state=StepConnectWithAdmin.connect)

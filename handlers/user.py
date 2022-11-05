import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from core.messages import (ASK_NUMBER, ERROR_FULLNAME,
                           ERROR_PHONE, GREETING, ASK_FULLNAME, SETTING, SETTINGS_MESSAGE, BACK, SET_PHONE, SET_NAME,
                           ASK_NEW_PHONE, ASK_NEW_FULLNAME, SUCCESS_CHANGE_PHONE, SUCCESS_CHANGE_FULLNAME)
from create_bot import dp
from keyboards.start import KbStart
from keyboards.user import KbSetUser
from models.user import User


class UserRegForm(StatesGroup):
    full_name = State()
    phone = State()


def validate_phone(phone: str) -> bool:
    check_phone = bool(re.fullmatch("^(\+7[0-9]{10})$", phone))
    if check_phone:  # Формат: +79999999999
        return True
    return False


def validate_fullname(full_name: str) -> bool:
    check_full_name = bool(re.fullmatch("^[A-ЯЁ][а-яё]+\s[A-ЯЁ][а-яё]+$", full_name))
    if check_full_name:  # Формат: Иван Иванов
        return True
    return False


@dp.message_handler(state=UserRegForm.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    if validate_fullname(message.text):
        await state.update_data(name=message.text)
        await message.answer(text=ASK_NUMBER, parse_mode=ParseMode.MARKDOWN_V2)
        await UserRegForm.phone.set()
    else:
        await message.answer(text=ERROR_FULLNAME, parse_mode=ParseMode.MARKDOWN_V2)
        await UserRegForm.full_name.set()


@dp.message_handler(state=UserRegForm.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if validate_phone(message.text):
        await state.update_data(phone=message.text)
        data = await state.get_data()
        await User(
            user_id=state.user, full_name=data["name"], phone=data["phone"]
        ).create()
        await message.answer(
            text=GREETING, reply_markup=KbStart().get_main(), parse_mode=ParseMode.MARKDOWN_V2
        )

    else:
        await message.answer(text=ERROR_PHONE, parse_mode=ParseMode.MARKDOWN_V2)
        await UserRegForm.phone.set()


async def create_user(message: types.Message):
    await message.answer(text=ASK_FULLNAME, parse_mode=ParseMode.MARKDOWN_V2)
    await UserRegForm.full_name.set()


class ChanceUserForm(StatesGroup):
    full_name = State()
    phone = State()


async def start_edit_user(message: types.Message):
    await message.answer(text=SETTINGS_MESSAGE, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=KbSetUser().get_main())


async def get_callback_start(call: types.CallbackQuery):
    if call.data == SET_NAME:
        await ChanceUserForm.full_name.set()
        await call.message.answer(text=ASK_NEW_FULLNAME, parse_mode=ParseMode.MARKDOWN_V2)

    elif call.data == SET_PHONE:
        await ChanceUserForm.phone.set()
        await call.message.answer(text=ASK_NEW_PHONE, parse_mode=ParseMode.MARKDOWN_V2)

    elif call.data == BACK:
        await call.message.answer(text=GREETING, reply_markup=KbStart().get_main(), parse_mode=ParseMode.MARKDOWN_V2)
    await call.answer()


async def chance_phone(message: types.Message, state: FSMContext):
    if validate_phone(message.text):
        await User(user_id=message.from_user.id, phone=message.text).chance_phone_by_id()
        await state.finish()
        await message.answer(
            text=SUCCESS_CHANGE_PHONE,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=KbStart().get_main())
    else:
        await message.answer(text=ERROR_PHONE, parse_mode=ParseMode.MARKDOWN_V2)


async def chance_full_name(message: types.Message, state: FSMContext):
    if validate_fullname(message.text):
        await User(user_id=message.from_user.id, full_name=message.text).chance_fullname_by_id()
        await state.finish()
        await message.answer(
            text=SUCCESS_CHANGE_FULLNAME,
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=KbStart().get_main())
    else:
        await message.answer(text=ERROR_PHONE, parse_mode=ParseMode.MARKDOWN_V2)


def register_handlers_edit(dp: Dispatcher):
    dp.register_message_handler(start_edit_user, Text(equals=SETTING))
    dp.register_callback_query_handler(get_callback_start, Text(equals=[SET_NAME, SET_PHONE, BACK]))
    dp.register_message_handler(chance_phone, state=ChanceUserForm.phone)
    dp.register_message_handler(chance_full_name, state=ChanceUserForm.full_name)

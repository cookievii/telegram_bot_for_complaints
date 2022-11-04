import re

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from core.messages import ERROR_FULLNAME, ASK_NUMBER, ERROR_PHONE, GREETING, ASK_FULLNAME
from create_bot import dp
from keyboards.registration import KeyboardReg
from models.user import User


async def start(message: types.Message):
    is_registered = await User(user_id=message.from_user.id).exists()
    if is_registered:
        await message.answer(GREETING, reply_markup=KeyboardReg().get_main(), parse_mode="MarkdownV2")
    else:
        await message.answer(ASK_FULLNAME, parse_mode="MarkdownV2")
        await FormUser.full_name.set()


def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"])


class FormUser(StatesGroup):
    full_name = State()
    phone = State()


def validate_phone(phone):
    check_phone = bool(re.fullmatch('^(\+7[0-9]{10})$', phone))
    if check_phone:  # Формат: +79999999999
        return True
    return False


def validate_fullname(full_name):
    check_full_name = bool(re.fullmatch('^[A-ЯЁ][а-яё]+\s[A-ЯЁ][а-яё]+$', full_name))
    if check_full_name:  # Формат: Иван Иванов
        return True
    return False


@dp.message_handler(state=FormUser.full_name)
async def get_full_name(message: types.Message, state: FSMContext):
    if validate_fullname(message.text):
        await state.update_data(name=message.text)
        await message.answer(ASK_NUMBER, parse_mode="MarkdownV2")
        await FormUser.phone.set()
    else:
        await message.answer(ERROR_FULLNAME, parse_mode="MarkdownV2")
        await FormUser.full_name.set()


@dp.message_handler(state=FormUser.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if validate_phone(message.text):
        await state.update_data(phone=message.text)
        data = await state.get_data()
        await User(user_id=state.user, full_name=data['name'], phone=data['phone']).create()
        await message.answer(GREETING, reply_markup=KeyboardReg().get_main(), parse_mode="MarkdownV2")

    else:
        await message.answer(ERROR_PHONE, parse_mode="MarkdownV2")
        await FormUser.phone.set()

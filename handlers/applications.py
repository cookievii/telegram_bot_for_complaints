import os

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType, ParseMode

from core.messages import APPLICATION, ASK_APP, GREETING, BACK_TO_MAIN, ASK_ADDRESS, \
    CONFIRM_APP, SKIP, ASK_MEDIA, BACK, ERROR_PHOTO, ASK_DESCRIPTION, SUCCESSFUL_CONFIRM_APP, SEND_COMPLAINT
from create_bot import bot
from keyboards.applications import KeyboardApp
from keyboards.registration import KeyboardReg
from models.user import User


class ConfirmAppState(StatesGroup):
    address = State()
    media = State()
    description = State()


async def leave_request_menu(message: types.Message):
    await message.answer(ASK_APP, reply_markup=KeyboardApp().get_application(), parse_mode="MarkdownV2")


async def get_callback_greeting(call: types.CallbackQuery):
    if call.data == BACK_TO_MAIN:
        await call.message.answer(GREETING, reply_markup=KeyboardReg().get_main(), parse_mode="MarkdownV2")

    elif call.data == CONFIRM_APP:
        await call.message.answer(ASK_ADDRESS, reply_markup=KeyboardApp().get_skip_and_back(), parse_mode="MarkdownV2")
        await ConfirmAppState.address.set()
    await call.answer()


async def get_callback_address(call: types.CallbackQuery, state: FSMContext):
    if call.data == SKIP:
        await call.message.answer(ASK_MEDIA, reply_markup=KeyboardApp().get_skip_and_back(), parse_mode="MarkdownV2")
        await ConfirmAppState.next()

    elif call.data == BACK:
        await state.finish()
        await call.message.answer(ASK_APP, reply_markup=KeyboardApp().get_application(), parse_mode="MarkdownV2")
    await call.answer()


async def get_message_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(ASK_MEDIA, reply_markup=KeyboardApp().get_skip_and_back(), parse_mode="MarkdownV2")
    await ConfirmAppState.next()


async def get_callback_media(call: types.CallbackQuery):
    if call.data == SKIP:
        await call.message.answer(ASK_DESCRIPTION, reply_markup=KeyboardApp().get_back(), parse_mode="MarkdownV2")
        await ConfirmAppState.next()
    elif call.data == BACK:
        await call.message.answer(ASK_ADDRESS, reply_markup=KeyboardApp().get_skip_and_back(), parse_mode="MarkdownV2")
        await ConfirmAppState.previous()
    await call.answer()


async def get_message_media(message: types.Message, state: FSMContext):
    if True in (bool(message.photo), bool(message.video)):
        if bool(message.photo) is True:
            await state.update_data(media=message.photo[-1])
        elif bool(message.video) is True:
            await state.update_data(media=message.video)
        await message.answer(ASK_DESCRIPTION, reply_markup=KeyboardApp().get_back(), parse_mode="MarkdownV2")
        await ConfirmAppState.description.set()

    else:
        await message.answer(ERROR_PHOTO)


async def get_callback_description(call: types.CallbackQuery):
    if call.data == BACK:
        await call.message.answer(ASK_MEDIA, reply_markup=KeyboardApp().get_skip_and_back(), parse_mode="MarkdownV2")
        await ConfirmAppState.previous()
    await call.answer()


async def get_message_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)

    chat_id = os.getenv("COMPLAINT_GROUP")
    user = await User(user_id=message.from_user.id).get_by_id()
    data = await state.get_data()
    text = SEND_COMPLAINT.format(
        tg_username=message.from_user.username,
        full_name=user.full_name,
        phone=user.phone,
        address=data.get('address', ''),
        description=data.get('description', ''))

    if data.get('media') is None or 'file_id' not in data.get('media'):
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
    else:
        await bot.send_photo(chat_id=chat_id, photo=data['media']['file_id'], caption=text, parse_mode=ParseMode.HTML)
    await state.finish()
    await message.answer(SUCCESSFUL_CONFIRM_APP, reply_markup=KeyboardReg().get_main(), parse_mode="MarkdownV2")


def register_handlers_application(dp: Dispatcher):
    dp.register_message_handler(leave_request_menu, Text(equals=APPLICATION))
    dp.register_callback_query_handler(get_callback_greeting, Text(equals=[BACK_TO_MAIN, CONFIRM_APP]))
    dp.register_callback_query_handler(get_callback_address, state=ConfirmAppState.address)
    dp.register_message_handler(get_message_address, content_types=ContentType.TEXT, state=ConfirmAppState.address)
    dp.register_callback_query_handler(get_callback_media, state=ConfirmAppState.media)
    dp.register_message_handler(get_message_media, content_types=ContentType.ANY, state=ConfirmAppState.media)
    dp.register_callback_query_handler(get_callback_description, state=ConfirmAppState.description)
    dp.register_message_handler(get_message_description, content_types=ContentType.TEXT,
                                state=ConfirmAppState.description)

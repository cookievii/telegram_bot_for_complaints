import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, ParseMode

from core.messages import (APPLICATION, ASK_ADDRESS, ASK_COMPLAINT,
                           ASK_DESCRIPTION, ASK_MEDIA, BACK, BACK_TO_MAIN,
                           LEAVE_REQUEST, ERROR_PHOTO, GREETING, SEND_COMPLAINT,
                           SKIP, SUCCESSFUL_CONFIRM_APP, SHARE_IN_OFFER, OFFER_MESSAGE, ERROR_NON_TEXT, SEND_OFFER)
from create_bot import bot
from keyboards.complaints import KbComplaint
from keyboards.registration import KbRegistration
from models.user import User


class ConfirmForm(StatesGroup):
    address = State()
    media = State()
    description = State()


class OfferForm(StatesGroup):
    description = State()
    photo = State()


async def start_confirm(message: types.Message):
    await message.answer(
        text=ASK_COMPLAINT,
        reply_markup=KbComplaint().get_complaint(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def get_callback_greeting(call: types.CallbackQuery):
    if call.data == BACK_TO_MAIN:
        await call.message.answer(
            text=GREETING,
            reply_markup=KbRegistration().get_main(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )

    elif call.data == LEAVE_REQUEST:
        await call.message.answer(
            text=ASK_ADDRESS,
            reply_markup=KbComplaint().get_skip_and_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await ConfirmForm.address.set()
    elif call.data == SHARE_IN_OFFER:
        await call.message.answer(
            text=OFFER_MESSAGE,
            reply_markup=KbComplaint().get_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await OfferForm.description.set()
    await call.answer()


async def get_callback_address(call: types.CallbackQuery, state: FSMContext):
    if call.data == SKIP:
        await call.message.answer(
            text=ASK_MEDIA,
            reply_markup=KbComplaint().get_skip_and_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await ConfirmForm.next()

    elif call.data == BACK:
        await state.finish()
        await call.message.answer(
            text=ASK_COMPLAINT,
            reply_markup=KbComplaint().get_complaint(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    await call.answer()


async def get_message_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer(
        text=ASK_MEDIA,
        reply_markup=KbComplaint().get_skip_and_back(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )
    await ConfirmForm.next()


async def get_callback_media(call: types.CallbackQuery):
    if call.data == SKIP:
        await call.message.answer(
            text=ASK_DESCRIPTION,
            reply_markup=KbComplaint().get_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await ConfirmForm.next()
    elif call.data == BACK:
        await call.message.answer(
            text=ASK_ADDRESS,
            reply_markup=KbComplaint().get_skip_and_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await ConfirmForm.previous()
    await call.answer()


async def get_message_media(message: types.Message, state: FSMContext):
    if True in (bool(message.photo), bool(message.video)):
        if bool(message.photo) is True:
            await state.update_data(media=message.photo[-1])
        elif bool(message.video) is True:
            await state.update_data(media=message.video)
        await message.answer(
            text=ASK_DESCRIPTION,
            reply_markup=KbComplaint().get_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await ConfirmForm.description.set()

    else:
        await message.answer(ERROR_PHOTO)


async def get_callback_description(call: types.CallbackQuery):
    if call.data == BACK:
        await call.message.answer(
            text=ASK_MEDIA,
            reply_markup=KbComplaint().get_skip_and_back(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
        await ConfirmForm.previous()
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
        address=data.get("address", ""),
        description=data.get("description", ""),
    )

    if data.get("media") is None or "file_id" not in data.get("media"):
        await bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)
    else:
        await bot.send_photo(
            chat_id=chat_id,
            photo=data["media"]["file_id"],
            caption=text,
            parse_mode=ParseMode.HTML,
        )
    await state.finish()
    await message.answer(
        text=SUCCESSFUL_CONFIRM_APP,
        reply_markup=KbRegistration().get_main(),
        parse_mode=ParseMode.MARKDOWN_V2,
    )


async def get_callback_offer(call: types.CallbackQuery, state: FSMContext):
    if call.data == BACK:
        await state.finish()
        await call.message.answer(
            text=ASK_COMPLAINT,
            reply_markup=KbComplaint().get_complaint(),
            parse_mode=ParseMode.MARKDOWN_V2,
        )
    await call.answer()


async def get_message_offer(message: types.Message, state: FSMContext):
    chat_id = os.getenv("OFFERS_GROUP")
    user = await User(user_id=message.from_user.id).get_by_id()

    if message.photo:
        if 'caption' in message.values:
            await state.update_data(description=message.values.get('caption', ''))
            await bot.send_photo(
                chat_id=chat_id,
                photo=message.photo[-1].file_id,
                caption=SEND_OFFER.format(
                    tg_username=message.from_user.username,
                    full_name=user.full_name,
                    phone=user.phone,
                    description=message.values.get("caption", "")),
                parse_mode=ParseMode.HTML)

    elif message.text:
        await bot.send_message(
            chat_id=chat_id,
            text=SEND_OFFER.format(
                tg_username=message.from_user.username,
                full_name=user.full_name,
                phone=user.phone,
                description=message.text),
            parse_mode=ParseMode.HTML)

    await state.finish()
    await message.answer(
        text=SUCCESSFUL_CONFIRM_APP,
        reply_markup=KbRegistration().get_main(),
        parse_mode=ParseMode.MARKDOWN_V2)


async def get_non_media_offer(message: types.Message):
    await message.delete()
    await message.answer(text=ERROR_NON_TEXT)


def register_handlers_complaint(dp: Dispatcher):
    dp.register_message_handler(start_confirm, Text(equals=APPLICATION))
    dp.register_callback_query_handler(
        get_callback_greeting, Text(equals=[BACK_TO_MAIN, LEAVE_REQUEST, SHARE_IN_OFFER])
    )
    dp.register_callback_query_handler(
        get_callback_address, state=ConfirmForm.address
    )
    dp.register_message_handler(
        get_message_address,
        content_types=ContentType.TEXT,
        state=ConfirmForm.address,
    )
    dp.register_callback_query_handler(get_callback_media, state=ConfirmForm.media)
    dp.register_message_handler(
        get_message_media, content_types=ContentType.ANY, state=ConfirmForm.media
    )
    dp.register_callback_query_handler(
        get_callback_description, state=ConfirmForm.description
    )
    dp.register_message_handler(
        get_message_description,
        content_types=ContentType.TEXT,
        state=ConfirmForm.description,
    )
    dp.register_callback_query_handler(get_callback_offer, state=OfferForm.description)
    dp.register_message_handler(get_message_offer, content_types=[ContentType.TEXT, ContentType.PHOTO],
                                state=OfferForm.description)
    dp.register_message_handler(get_non_media_offer, content_types=ContentType.ANY,
                                state=OfferForm.description)

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode

from core.messages import INFORMATION, CONTACTS
from keyboards.start import KbStart


async def information(message: types.Message):
    await message.answer(text=CONTACTS, reply_markup=KbStart().get_main(), parse_mode=ParseMode.HTML)


def register_handlers_information(db: Dispatcher):
    db.register_message_handler(information, Text(equals=INFORMATION))

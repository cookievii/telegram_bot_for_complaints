from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from core.messages import APPLICATION, ASK_APPLICATION
from keyboards.applications import Keyboard


async def main_menu(message: types.Message):
    await message.answer(ASK_APPLICATION, reply_markup=Keyboard().get_application())


# , parse_mode="MarkdownV2"

def register_handlers_application(dp: Dispatcher):
    dp.register_message_handler(main_menu, Text(equals=APPLICATION))

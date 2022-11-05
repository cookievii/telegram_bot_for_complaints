from aiogram.types import InlineKeyboardButton, KeyboardButton

from core.messages import (LEAVE_REQUEST, SHARE_IN_OFFER, BACK_TO_MAIN, SKIP, BACK, APPLICATION, CONTACT, SETTING,
                           INFORMATION, SET_PHONE, SET_NAME)

confirm_app = InlineKeyboardButton(text=LEAVE_REQUEST, callback_data=LEAVE_REQUEST)
share_in_offer = InlineKeyboardButton(text=SHARE_IN_OFFER, callback_data=SHARE_IN_OFFER)
back_to_main = InlineKeyboardButton(text=BACK_TO_MAIN, callback_data=BACK_TO_MAIN)

# Общие
skip = InlineKeyboardButton(text=SKIP, callback_data=SKIP)
back = InlineKeyboardButton(text=BACK, callback_data=BACK)

# Кнопки главного меню - KbStart
application = KeyboardButton(text=APPLICATION)
contact = KeyboardButton(text=CONTACT)
setting = KeyboardButton(text=SETTING)
info = KeyboardButton(text=INFORMATION)

# Кнопки изменения данных пользователя - KbSetUser
set_phone = InlineKeyboardButton(SET_PHONE, callback_data=SET_PHONE)
set_name = InlineKeyboardButton(SET_NAME, callback_data=SET_NAME)

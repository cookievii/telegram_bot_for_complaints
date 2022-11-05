from aiogram.types import InlineKeyboardButton, KeyboardButton

from core.messages import (LEAVE_REQUEST, SHARE_IN_OFFER, SKIP, BACK, APPLICATION, CONTACT, SETTING,
                           INFORMATION, SET_PHONE, SET_NAME, CALL_ME, COMMUNICATE_ADMIN, YES, INCORRECT_PHONE,
                           CLOSE_CONNECT)

confirm_app = InlineKeyboardButton(text=LEAVE_REQUEST, callback_data=LEAVE_REQUEST)
share_in_offer = InlineKeyboardButton(text=SHARE_IN_OFFER, callback_data=SHARE_IN_OFFER)

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

# Кнопки коммуникации - KbCommunicate
call_me = InlineKeyboardButton(CALL_ME, callback_data=CALL_ME)
communicate_with_admin = InlineKeyboardButton(COMMUNICATE_ADMIN, callback_data=COMMUNICATE_ADMIN)

yes = InlineKeyboardButton(YES, callback_data=YES)
incorrect_phone = InlineKeyboardButton(INCORRECT_PHONE, callback_data=INCORRECT_PHONE)

close_connect = InlineKeyboardButton(CLOSE_CONNECT, callback_data=CLOSE_CONNECT)

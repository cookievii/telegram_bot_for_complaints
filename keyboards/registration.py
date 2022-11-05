from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from core.messages import APPLICATION, CONTACT, INFORMATION, SETTING


class KbRegistration:
    # Кнопки для главного меню.
    application = KeyboardButton(text=APPLICATION)
    contact = KeyboardButton(text=CONTACT)
    setting = KeyboardButton(text=SETTING)
    info = KeyboardButton(text=INFORMATION)

    def get_main(self):
        return ReplyKeyboardMarkup(
            keyboard=[[self.application, self.contact], [self.setting], [self.info]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

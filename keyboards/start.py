from aiogram.types import ReplyKeyboardMarkup

from core.buttons import application, contact, info, setting


class KbStart:
    @staticmethod
    def get_main():
        return ReplyKeyboardMarkup(
            keyboard=[[application, contact], [setting], [info]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

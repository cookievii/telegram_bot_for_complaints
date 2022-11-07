from aiogram.types import ReplyKeyboardMarkup

from core.buttons import application, contact, info, setting


class KbStart:
    """Клавиатура главного меню."""

    @staticmethod
    def get_main():
        """Вернуть клавиатуру главного меню."""
        return ReplyKeyboardMarkup(
            keyboard=[[application, contact], [setting], [info]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

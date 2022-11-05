from aiogram.types import InlineKeyboardMarkup

from core.buttons import confirm_app, share_in_offer, back_to_main, skip, back


class KbComplaint:

    @staticmethod
    def get_complaint():
        return InlineKeyboardMarkup().add(confirm_app, share_in_offer).add(back_to_main)

    @staticmethod
    def get_skip_and_back():
        return InlineKeyboardMarkup().add(skip).add(back)

    @staticmethod
    def get_back():
        return InlineKeyboardMarkup().add(back)

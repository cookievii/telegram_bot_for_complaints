from aiogram.types import InlineKeyboardMarkup

from core.buttons import confirm_app, share_in_offer, skip, back


class KbComplaint:

    @staticmethod
    def get_main():
        return InlineKeyboardMarkup().add(confirm_app, share_in_offer).add(back)

    @staticmethod
    def get_skip_and_back():
        return InlineKeyboardMarkup().add(skip).add(back)

    @staticmethod
    def get_back():
        return InlineKeyboardMarkup().add(back)

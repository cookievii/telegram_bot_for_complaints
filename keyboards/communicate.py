from aiogram.types import InlineKeyboardMarkup

from core.buttons import back, call_me, communicate_with_admin, yes, incorrect_phone, close_connect


class KbCommunicate:
    @staticmethod
    def get_main():
        return InlineKeyboardMarkup().add(call_me).add(communicate_with_admin).add(back)

    @staticmethod
    def get_check_phone_menu():
        return InlineKeyboardMarkup().add(yes).add(incorrect_phone)

    @staticmethod
    def get_close_connect():
        return InlineKeyboardMarkup().add(close_connect)

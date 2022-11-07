from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup

from core.buttons import back_admin, permission, search_user, spam_msg


class KbAdmin:
    @staticmethod
    def get_main():
        return ReplyKeyboardMarkup(
            keyboard=[[search_user], [spam_msg], [permission]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )

    @staticmethod
    def get_back_and_permission():
        return InlineKeyboardMarkup().add(permission).add(back_admin)

    @staticmethod
    def get_back():
        return InlineKeyboardMarkup().add(back_admin)

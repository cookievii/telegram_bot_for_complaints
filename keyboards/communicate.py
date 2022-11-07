from aiogram.types import InlineKeyboardMarkup

from core.buttons import (back, call_me, close_connect, communicate_with_admin,
                          incorrect_phone, yes)


class KbCommunicate:
    """Инлайн-кнопки коммуникации."""

    @staticmethod
    def get_main():
        """Возвращает Инлайн-кнопки: "связи с администратором", "позвонить мне" и "назад"."""
        return InlineKeyboardMarkup().add(call_me).add(communicate_with_admin).add(back)

    @staticmethod
    def get_check_phone_menu():
        """Возвращает Инлайн-кнопки: "Да", "Некорректный номер телефона"."""
        return InlineKeyboardMarkup().add(yes).add(incorrect_phone)

    @staticmethod
    def get_close_connect():
        """Возвращает Инлайн-кнопки: "Завершить общение с администратором"."""
        return InlineKeyboardMarkup().add(close_connect)

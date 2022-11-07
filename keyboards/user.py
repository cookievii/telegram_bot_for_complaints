from aiogram.types import InlineKeyboardMarkup

from core.buttons import back, set_name, set_phone


class KbSetUser:
    """Инлайн-кнопки настройки пользователя."""

    @staticmethod
    def get_main():
        """Вернуть инлайн-кнопки "Сменить номер", "Сменить имя", "Назад"."""
        return InlineKeyboardMarkup().add(set_name, set_phone).add(back)

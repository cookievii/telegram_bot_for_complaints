from aiogram.types import InlineKeyboardMarkup

from core.buttons import back, confirm_app, share_in_offer, skip


class KbComplaint:
    """Инлайн-кнопки "Жалоб" и "Предложений"."""

    @staticmethod
    def get_main():
        """Возвращает инлайн-кнопки "оставить жалобу", "предложение" и "назад"."""
        return InlineKeyboardMarkup().add(confirm_app, share_in_offer).add(back)

    @staticmethod
    def get_skip_and_back():
        """Возвращает инлайн-кнопки "Пропустить" и "назад"."""
        return InlineKeyboardMarkup().add(skip).add(back)

    @staticmethod
    def get_back():
        """Возвращает инлайн-кнопку "назад"."""
        return InlineKeyboardMarkup().add(back)

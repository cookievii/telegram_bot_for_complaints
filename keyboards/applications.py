from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


class Keyboard(InlineKeyboardMarkup):
    application = InlineKeyboardButton(text="📛 Оставить заявку", callback_data="confirm_app")
    offer = InlineKeyboardButton(text="💡 Поделиться предложением", callback_data="offer")
    back = InlineKeyboardButton(text="🔙 Назад", callback_data="start")

    def get_application(self):
        return ReplyKeyboardMarkup(keyboard=self.add(
            [self.application, self.offer],
            self.back
        ), resize_keyboard=True, one_time_keyboard=True)

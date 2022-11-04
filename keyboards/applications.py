from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.messages import CONFIRM_APP, BACK_TO_MAIN, SHARE_IN_OFFER, SKIP, BACK


class KeyboardApp:
    confirm_app = InlineKeyboardButton(text=CONFIRM_APP, callback_data=CONFIRM_APP)
    share_in_offer = InlineKeyboardButton(text=SHARE_IN_OFFER, callback_data=SHARE_IN_OFFER)
    back_to_main = InlineKeyboardButton(text=BACK_TO_MAIN, callback_data=BACK_TO_MAIN)

    skip = InlineKeyboardButton(text=SKIP, callback_data=SKIP)
    back = InlineKeyboardButton(text=BACK, callback_data=BACK)

    def get_application(self):
        return InlineKeyboardMarkup().add(self.confirm_app, self.share_in_offer).add(self.back_to_main)

    def get_skip_and_back(self):
        return InlineKeyboardMarkup().add(self.skip).add(self.back)

    def get_back(self):
        return InlineKeyboardMarkup().add(self.back)

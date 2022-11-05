from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.messages import BACK, BACK_TO_MAIN, LEAVE_REQUEST, SHARE_IN_OFFER, SKIP


class KbComplaint:
    confirm_app = InlineKeyboardButton(text=LEAVE_REQUEST, callback_data=LEAVE_REQUEST)
    share_in_offer = InlineKeyboardButton(
        text=SHARE_IN_OFFER, callback_data=SHARE_IN_OFFER
    )
    back_to_main = InlineKeyboardButton(text=BACK_TO_MAIN, callback_data=BACK_TO_MAIN)

    skip = InlineKeyboardButton(text=SKIP, callback_data=SKIP)
    back = InlineKeyboardButton(text=BACK, callback_data=BACK)

    def get_complaint(self):
        return (
            InlineKeyboardMarkup()
            .add(self.confirm_app, self.share_in_offer)
            .add(self.back_to_main)
        )

    def get_skip_and_back(self):
        return InlineKeyboardMarkup().add(self.skip).add(self.back)

    def get_back(self):
        return InlineKeyboardMarkup().add(self.back)

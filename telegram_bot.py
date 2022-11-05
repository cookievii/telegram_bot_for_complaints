from aiogram.utils import executor

from create_bot import dp
from models.datebase import cretae_db

if __name__ == "__main__":
    # Запуск bd
    cretae_db()

    # Запуск бота
    from handlers import complaints, registration

    registration.register_handlers_registration(dp)
    complaints.register_handlers_complaint(dp)

    executor.start_polling(dp, skip_updates=True)

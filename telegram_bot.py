from aiogram.utils import executor

from create_bot import dp
from models.datebase import cretae_db

if __name__ == "__main__":
    # Создание БД\таблицы.
    cretae_db()

    # Регистрация handlers.
    from handlers import complaint, start, information, user, communicate

    start.register_handlers_start(dp)  # Главное меню.
    complaint.register_handlers_complaint(dp)  # Жалобы и предложения.
    information.register_handlers_information(dp)  # Информация о компания.
    user.register_handlers_edit(dp)  # Изменение данных пользователя.
    communicate.register_handlers_contact(dp)  # Обратная связь и связь с администратором.

    # Запуск бота.
    executor.start_polling(dp, skip_updates=True)

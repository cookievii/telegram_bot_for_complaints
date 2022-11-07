from aiogram.utils import executor

from create_bot import dp
from models.datebase import create_db


def on_start() -> None:
    print("Бот работает!)")


if __name__ == "__main__":
    # Создание БД\таблицы.
    create_db()

    # Регистрация handlers.
    from handlers import (admin, communicate, complaint, information, start,
                          user)

    start.register_handlers_start(dp)  # Start.
    admin.register_handlers_admin(dp)  # Администрирование.
    complaint.register_handlers_complaint(dp)  # Жалобы и предложения.
    information.register_handlers_information(dp)  # Информация о компания.
    user.register_handlers_edit(dp)  # Изменение данных пользователя.
    communicate.register_handlers_contact(dp)  # Связь с администратором.

    # Запуск бота.
    executor.start_polling(dp, skip_updates=True, on_startup=on_start())

from config import BOT_TOKEN, admin_id, admin_id_main
from database.db import (does_tables_exist,
                         create_tables)
from handlers.common_handlers import cancel_router, common_router
from handlers.survey_handlers import survey_router
from handlers.admin_handlers import admin_router

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand


ADMIN_IDS = [admin_id, admin_id_main]

# Включаем логирование, чтобы видеть что происходит
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Инициализируем бота и диспетчер
logger = logging.getLogger('main_logger')
storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


dp.include_router(cancel_router)
dp.include_router(survey_router)
dp.include_router(common_router)
dp.include_router(admin_router)

# Главная асинхронная функция
async def main():
    """
    Запуск бота
    """
    # Запускаем polling (постоянный опрос серверов Telegram)
    logger.info('Бот запущен')
    # Установка команд бота
    await bot.set_my_commands([
        BotCommand(command="/start", description="Начать"),
        BotCommand(command="/cancel", description="Отменить текущее действие")
    ])
    await dp.start_polling(bot)


# Точка входа в программу
if __name__ == "__main__":
    # Инициализация БД - теперь синхронно
    try:
        # Синхронная проверка и создание таблиц
        if not does_tables_exist():
            try:
                create_tables()
                logger.info('Таблицы успешно созданы в базе данных')
            except Exception as e:
                logger.error(f'Ошибка создания таблиц: {e}')
        else:
            logger.info('Таблицы уже существуют')

        # Запускаем бота
        asyncio.run(main())

    except KeyboardInterrupt:
        logger.info('Бот остановлен')
    except Exception as e:
        logger.error(f'Ошибка запуска бота: {e}')
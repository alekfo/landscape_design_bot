from config import admin_id, admin_id_main
from database.models import Client
from keyboards.keyboards import (get_сalculation_keyboard,
                                 get_type_of_work_keyboard,
                                 get_size_of_plot_keyboard,
                                 get_condition_of_plot_keyboard,
                                 get_class_of_work_keyboard,
                                 get_period_of_start_keyboard,
                                 get_number_keyboard,
                                 return_keyboard,
                                 take_admin_choise_keyboard)
from database.db import create_client, got_clients_in_chat, get_all_clients_from_db
from states import UserStates, AdminStates
from handlers.common_handlers import cancel_handler

from datetime import datetime
import openpyxl
from io import BytesIO
import logging
from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import SQLAlchemyError
from aiogram.types import FSInputFile, BufferedInputFile

from aiogram.types import ReplyKeyboardRemove

logger = logging.getLogger(__name__)
admin_router = Router()

@admin_router.message(StateFilter(AdminStates.choise_action))
async def processed_admin_actions(message: types.Message, state: FSMContext):

    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    if message.text == 'Выгрузка в чат':
        res = got_clients_in_chat()
        await message.answer(
            f"Последние 20 заявок:\n\n{res}",
            reply_markup=return_keyboard()
        )
        await state.set_state(AdminStates.clients_gotten)
    elif message.text == 'Выгрузка файлом':
        file_stream = await got_clients_in_file()
        if file_stream:
            # Создаем BufferedInputFile из BytesIO
            excel_file = BufferedInputFile(
                file=file_stream.getvalue(),
                filename=f"clients_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            )

            await message.answer_document(
                document=excel_file,
                caption="📊 Файл со всеми заявками",
                reply_markup=return_keyboard()
            )
        else:
            logger.error(f"Ошибка создания файла")
            await message.answer(
                "❌ Ошибка при создании файла",
                reply_markup=return_keyboard()
            )
        await state.set_state(AdminStates.clients_gotten)
    else:
        await message.answer(
            f"Пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=take_admin_choise_keyboard()
        )


@admin_router.message(StateFilter(AdminStates.clients_gotten))
async def processed_return(message: types.Message, state: FSMContext):

    if message.text == 'Вернуться':
        await message.answer(
            f'Выберите действие🚀',
            reply_markup=take_admin_choise_keyboard()
        )
        await state.set_state(AdminStates.choise_action)
    else:
        await message.answer(
            f"Пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=return_keyboard()
        )

async def got_clients_in_file():
    """Создает Excel файл с клиентами и возвращает его как BytesIO"""
    try:
        # Получаем всех клиентов
        clients = get_all_clients_from_db()

        # Создаем Excel файл
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Клиенты"

        # Заголовки
        headers = ['ID', 'Имя', 'ID пользователя', 'Тип работ', 'Размер участка',
                   'Состояние', 'Класс работ', 'Период старта', 'Телефон', 'Скидка', 'Дата']
        ws.append(headers)

        # Данные
        for client in clients:
            ws.append([
                client.id,
                client.clients_name,
                client.clients_id,
                client.type_of_work,
                client.plots_size,
                client.plots_condition,
                client.class_of_work,
                client.period_of_start,
                client.clients_number,
                'Да' if client.discount else 'Нет',
                client.current_date.strftime('%Y-%m-%d') if client.current_date else ''
            ])

        # Сохраняем в BytesIO
        file_stream = BytesIO()
        wb.save(file_stream)
        file_stream.seek(0)

        return file_stream

    except Exception as e:
        logger.error(f"Ошибка создания файла: {e}")
        return None
from keyboards.keyboards import get_сalculation_keyboard, take_admin_choise_keyboard
from database.db import does_clients_exists
from states import UserStates, AdminStates
from config import admin_id_main, admin_id

import logging
from aiogram import types, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart


logger = logging.getLogger(__name__)
common_router = Router()
cancel_router = Router()

ADMIN_IDS = [admin_id, admin_id_main]

@common_router.message(CommandStart())
@common_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Этот обработчик срабатывает на команду /start и при первом входе
    """
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    if user_id in ADMIN_IDS:
        await message.answer(
            f'Вы яляетесь администратором чат-бота\n\n'
            f'Выберите действие🚀',
            reply_markup=take_admin_choise_keyboard()
        )
        await state.set_state(AdminStates.choise_action)
        return

    # Сохраняем данные пользователя в state
    await state.update_data(
        clients_id=user_id
    )

    # Проверяем, существует ли пользователь в БД
    user_exists = does_clients_exists(user_id)

    if user_exists:
        await message.answer(
            f'Рады снова приветствовать Вас, {user_name}, в компании "ЭкоЛандшафт"!🌳\n\n'
            'Чтобы повторно заполнить форму, воспользуйтесь кнопкой ниже🚀',
            reply_markup=get_сalculation_keyboard()
        )
    else:
        await message.answer(
            'Мы рады приветствовать Вас в компании "ЭкоЛандшафт"!🌳\n'
            'В основном мы создаём участки под ключ от проекта до реализации, '
            'но Вы можете заказать отдельные виды работ.\n\n'
            'Хотите рассчитаю предварительную стоимость?💰',
            reply_markup=get_сalculation_keyboard()
        )
        # Логируем нового пользователя
        logger.info(f'Новый пользователь бота: user_name: {user_name}, user_id {user_id}')

    await state.set_state(UserStates.wait_for_start)

@common_router.message(StateFilter(None))
async def handle_any_message(message: types.Message, state: FSMContext):
    """Обработчик любых сообщений без состояния"""
    await cmd_start(message, state)


@cancel_router.message(Command("cancel"))
@cancel_router.message(lambda message: message.text == "Отмена")
async def cancel_handler(message: types.Message, state: FSMContext):
    """Сброс состояния"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Действие отменено.",
        reply_markup=types.ReplyKeyboardRemove()
    )
    await cmd_start(message, state)
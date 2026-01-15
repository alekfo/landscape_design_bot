from config import admin_id, admin_id_main
from database.models import Client
from keyboards.keyboards import (get_сalculation_keyboard,
                                 get_type_of_work_keyboard,
                                 get_size_of_plot_keyboard,
                                 get_condition_of_plot_keyboard,
                                 get_class_of_work_keyboard,
                                 get_period_of_start_keyboard,
                                 get_number_keyboard, cancel_keyboard)
from database.db import create_client
from states import UserStates
from handlers.common_handlers import cancel_handler

import logging
from aiogram import types, F, Router, Bot
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import SQLAlchemyError

from aiogram.types import ReplyKeyboardRemove

ADMIN_IDS = [admin_id, admin_id_main]

logger = logging.getLogger(__name__)
survey_router = Router()

@survey_router.message(StateFilter(UserStates.wait_for_start))
async def choise_type_of_work(message: types.Message, state: FSMContext):

    if message.text == 'Калькулятор стоимости':
        await state.set_state(UserStates.get_client_name)
        await message.answer(
            "Как к Вам обращаться?",
            reply_markup=cancel_keyboard()
        )
    else:
        await message.answer(
            f"Чтобы отправить ответ, пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=get_сalculation_keyboard()
        )


@survey_router.message(StateFilter(UserStates.get_client_name))
async def get_client_name_handler(message: types.Message, state: FSMContext):
    """Получаем настоящее ФИО клиента"""
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    # Проверяем, что введено не слишком короткое имя
    if len(message.text.strip()) < 3:
        await message.answer(
            "Пожалуйста, введите ваше полное имя (минимум 3 символа):",
            reply_markup=cancel_keyboard()
        )
        return

    # Сохраняем ФИО
    await state.update_data(clients_name=message.text.strip())

    # Переходим к выбору типа работ
    await state.set_state(UserStates.start_survey)
    await message.answer(
        f"Спасибо! Какие виды работ вас интересуют?",
        reply_markup=get_type_of_work_keyboard()
    )

@survey_router.message(StateFilter(UserStates.start_survey))
async def choise_size_of_plot(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    check_list = ['Проект', 'Ландшафт под ключ', 'Озеленение', 'Отдельные виды работ']
    if message.text in check_list:

        user_data = await state.get_data()
        if 'type_of_work' not in user_data:
            await state.update_data(
                type_of_work=message.text
            )

        await state.set_state(UserStates.get_size_of_plot)
        await message.answer(
            f"Укажите размер вашего участка",
            reply_markup=get_size_of_plot_keyboard()
        )
    else:
        await message.answer(
            f"Чтобы отправить ответ, пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=get_type_of_work_keyboard()
        )

@survey_router.message(StateFilter(UserStates.get_size_of_plot))
async def choise_condition_of_plot(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    check_list = ['Менее 5 соток', '5-15 соток', '15-25 соток', '25-50 соток', 'Свыше 50 соток']
    if message.text in check_list:

        user_data = await state.get_data()
        if 'plots_size' not in user_data:
            await state.update_data(
                plots_size=message.text
            )

        await state.set_state(UserStates.get_condition_of_plot)
        await message.answer(
            f"В каком сейчас состоянии участок?",
            reply_markup=get_condition_of_plot_keyboard()
        )
    else:
        await message.answer(
            f"Чтобы отправить ответ, пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=get_size_of_plot_keyboard()
        )

@survey_router.message(StateFilter(UserStates.get_condition_of_plot))
async def choise_class_of_work(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    check_list = ['Строится или построен дом, работы на участке не проводились',
                  'Строится или построен дом, некоторые работы по благоустройству выполнены',
                  'Планируется строительство дома',
                  'Обжитой участок, требуется его реновация']

    if message.text in check_list:

        user_data = await state.get_data()
        if 'plots_condition' not in user_data:
            await state.update_data(
                plots_condition=message.text
            )

        await state.set_state(UserStates.get_class_of_work)
        await message.answer(
            f"Какой вариант для вас предпочительнее?",
            reply_markup=get_class_of_work_keyboard()
        )
    else:
        await message.answer(
            f"Чтобы отправить ответ, пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=get_condition_of_plot_keyboard()
        )

@survey_router.message(StateFilter(UserStates.get_class_of_work))
async def choise_period_of_start(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    check_list = ['Бюджетно - минимальными затратами привести участок в порядок',
                  'Оптимально - важен баланс цена/качество',
                  'Роскошно - высокая плотность посадок, премиальные отделочные материалы']
    if message.text in check_list:

        user_data = await state.get_data()
        if 'class_of_work' not in user_data:
            await state.update_data(
                class_of_work=message.text
            )

        await state.set_state(UserStates.get_period_of_start)
        await message.answer(
            f"Когда хотели бы начать работы по проектированию?",
            reply_markup=get_period_of_start_keyboard()
        )
    else:
        await message.answer(
            f"Чтобы отправить ответ, пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=get_class_of_work_keyboard()
        )

@survey_router.message(StateFilter(UserStates.get_period_of_start))
async def clients_number(message: types.Message, state: FSMContext):
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    check_list = ['В ближайшее время',
                  'В течение нескольких месяцев',
                  'Пока просто прицениваюсь']
    if message.text in check_list:

        user_data = await state.get_data()
        if 'period_of_start' not in user_data:
            await state.update_data(
                period_of_start=message.text
            )

        await state.set_state(UserStates.get_clients_number)
        await message.answer(
            f"Куда отправить стоимость вашего проекта?",
            reply_markup=get_number_keyboard() # как сделать клавиатуру с получением номера юзера одной кнопкой
        )
    else:
        await message.answer(
            f"Чтобы отправить ответ, пожалуйста, воспользуйтесь кнопками\n\n"
            f"Если хотите закончить нажмите на кнопку - Отмена↩️",
            reply_markup=get_class_of_work_keyboard()
        )


@survey_router.message(StateFilter(UserStates.get_clients_number), F.contact)
async def get_contact(message: types.Message, state: FSMContext, bot: Bot):
    """Обработчик получения контакта"""
    if message.text and message.text.lower() == "отмена":
        await cancel_handler(message, state)
        return

    contact = message.contact
    if contact and contact.user_id == message.from_user.id:
        # Сохраняем номер
        await state.update_data(clients_number=contact.phone_number)

        # Получаем все данные
        user_data = await state.get_data()

        # Создаем клиента в БД
        try:
            # Подготовим данные для БД
            client_data = {
                'clients_name': user_data.get('clients_name', ''),
                'clients_id': str(user_data.get('clients_id', '')),
                'type_of_work': user_data.get('type_of_work', ''),
                'plots_size': user_data.get('plots_size', ''),
                'plots_condition': user_data.get('plots_condition', ''),
                'class_of_work': user_data.get('class_of_work', ''),
                'period_of_start': user_data.get('period_of_start', ''),
                'clients_number': contact.phone_number,
                'discount': True
            }
            try:
                # Создаем клиента в БД
                client: Client = create_client(client_data)

                # Логируем
                logger.info(f"Новый клиент: {client_data['clients_name']} (ID: {client_data['clients_id']})")

                # Отправляем сообщение админу

                admin_message = (
                    "👤*Новый клиент!*\n\n"
                    f"*Имя:* {client.clients_name}\n"
                    f"*ID:* {client.clients_id}\n"
                    f"*Тип работ:* {client.type_of_work}\n"
                    f"*Размер участка:* {client.plots_size}\n"
                    f"*Состояние:* {client.plots_condition}\n"
                    f"*Класс работ:* {client.class_of_work}\n"
                    f"*Период начала:* {client.period_of_start}\n"
                    f"*Телефон:* {client.clients_number}\n"
                )


                for admin_id_i in ADMIN_IDS:
                    try:
                        await bot.send_message(
                            chat_id=admin_id_i,
                            text=admin_message,
                            parse_mode="Markdown"
                        )
                        logger.info(f"Сообщение отправлено админу {admin_id_i}")
                    except Exception as e:
                        logger.error(f"Ошибка отправки админу {admin_id_i}: {e}")

                # await bot.send_message(
                #     chat_id=admin_id,
                #     text=admin_message,
                #     parse_mode="Markdown"
                # )

                # Сообщение пользователю
                await message.answer(
                    "✅Спасибо! Ваши данные сохранены.\n"
                    "Мы также дарим Вам скидку 10%, которая будет действительна в течение 30 дней по Вашему номеру.\n\n"
                    "Наш менеджер свяжется с вами в ближайшее время.📞",
                    reply_markup=ReplyKeyboardRemove()
                )

                # Сбрасываем состояние
                await state.clear()
            except SQLAlchemyError as e:
                logger.error(f"Ошибка SQLAlchemy при сохранении клиента: {e}", exc_info=True)
                await message.answer(
                    "❌ Ошибка базы данных. Попробуйте позже.",
                    reply_markup=ReplyKeyboardRemove()
                )

        except Exception as e:
            logger.error(f"Ошибка сохранения клиента: {e}", exc_info=True)
            await message.answer(
                "❌ Произошла ошибка при сохранении данных. Попробуйте позже.",
                reply_markup=ReplyKeyboardRemove()
            )
    else:
        await message.answer(
            "Пожалуйста, поделитесь своим номером телефона, нажав на кнопку ниже",
            reply_markup=get_number_keyboard()
        )
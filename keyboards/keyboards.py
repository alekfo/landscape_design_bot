from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

# Создаем клавиатуру для приветствия
def get_сalculation_keyboard():
    """
    Создает клавиатуру с кнопками "Калькулятор стоимости" и "Отмена"
    """
    builder = ReplyKeyboardBuilder()

    builder.row(
        types.KeyboardButton(text="Калькулятор стоимости")
    )

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

def get_type_of_work_keyboard():
    """Клавиатура для выбора типа работ"""
    keyboard = [
        [types.KeyboardButton(text="Проект")],
        [types.KeyboardButton(text="Ландшафт под ключ")],
        [types.KeyboardButton(text="Озеленение")],
        [types.KeyboardButton(text="Отдельные виды работ")],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_size_of_plot_keyboard():
    """Клавиатура для выбора размера участка"""
    keyboard = [
        [types.KeyboardButton(text="Менее 5 соток")],
        [types.KeyboardButton(text="5-15 соток")],
        [types.KeyboardButton(text="15-25 соток")],
        [types.KeyboardButton(text="25-50 соток")],
        [types.KeyboardButton(text="Свыше 50 соток")],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_condition_of_plot_keyboard():
    """Клавиатура для выбора состояния участка"""
    keyboard = [
        [types.KeyboardButton(text="Строится или построен дом, работы на участке не проводились")],
        [types.KeyboardButton(text="Строится или построен дом, некоторые работы по благоустройству выполнены")],
        [types.KeyboardButton(text="Планируется строительство дома")],
        [types.KeyboardButton(text="Обжитой участок, требуется его реновация")],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def get_class_of_work_keyboard():
    """Клавиатура для выбора класса работ"""
    keyboard = [
        [types.KeyboardButton(text="Бюджетно - минимальными затратами привести участок в порядок")],
        [types.KeyboardButton(text="Оптимально - важен баланс цена/качество")],
        [types.KeyboardButton(text="Роскошно - высокая плотность посадок, премиальные отделочные материалы")],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_period_of_start_keyboard():
    """Клавиатура для выбора периода старта"""
    keyboard = [
        [types.KeyboardButton(text="В ближайшее время")],
        [types.KeyboardButton(text="В течение нескольких месяцев")],
        [types.KeyboardButton(text="Пока просто прицениваюсь")],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_number_keyboard():
    """Клавиатура для получения номера телефона"""
    keyboard = [
        [types.KeyboardButton(
            text="📱 Отправить номер телефона",
            request_contact=True
        )],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Нажмите кнопку для отправки контакта"
    )

def take_admin_choise_keyboard():
    """Клавиатура для выбора дейсствия для админа"""
    keyboard = [
        [types.KeyboardButton(text="Выгрузка в чат")],
        [types.KeyboardButton(text="Выгрузка файлом")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def return_keyboard():
    """Клавиатура для возврата в меню админа"""
    keyboard = [
        [types.KeyboardButton(text="Вернуться")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

def cancel_keyboard():
    """Клавиатура с кнопкой отмена"""
    keyboard = [
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

# # Создаем клавиатуру для сообщения "в разработке"
# def get_back_keyboard():
#     """
#     Создает инлайн-клавиатуру с одной кнопкой "Продолжить"
#     """
#     builder = InlineKeyboardBuilder()
#     # Добавляем кнопку с callback_data - это данные, которые придут при нажатии
#     builder.add(types.InlineKeyboardButton(
#         text="← Вернуться",
#         callback_data="back"
#     ))
#     return builder.as_markup()
from aiogram.fsm.state import State, StatesGroup

# 2. Создаем класс состояний
class UserStates(StatesGroup):
    """Класс для хранения состояний клиента"""
    wait_for_start = State() # ожидание нажатия кнопки начала калькуляции
    get_client_name = State()
    start_survey = State() # начало опроса
    get_size_of_plot = State()
    get_condition_of_plot = State()
    get_class_of_work = State()
    get_period_of_start = State()
    get_clients_number = State()

class AdminStates(StatesGroup):
    """Класс для хранения состояний админа"""
    choise_action = State() # ожидание выбора действия от админа
    clients_gotten = State()# состояние после получения клиентов в выгрузке
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class AuditWay(StatesGroup):
    q1 = State() # Название предприятия
    q2 = State() # ИНН/УНП
    q3 = State() # Сайт
    q4 = State() # Особенности
    q5 = State() # Запрос/цель
    q6 = State() # Возможности
    q7 = State() # Телефон
    q8 = State() # Когда связаться


class Messages:
    steps = [
        "Название Вашего предприятия?",
        "ИНН (для РФ) или УНП (для РБ)?",
        "Ваш сайт?",
        "Кратко опишите особенности Ваших товаров или Вас как производителя",
        "Ваш запрос: задача, желание? Сформулируйте основной запрос – свои цели (цель)",
        "Ваши возможности. Вы уверены, что Ваших возможностей хватит на выполнение Вашего Запроса?",
        "Оставьте телефон для связи",
        "Когда будет удобно, чтобы мы связались с Вами?",
    ]

    done = (
        "Благодарю! Плановая обратная связь с Вами в течение 48 часов, чтобы назначить аудит потенциала «входа» в указанную торговую сеть. Он бесплатный и без продаж по телефону — обещаю 🤝"
    )


class Markups:
    wizard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Контакты для связи", callback_data="contacts")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
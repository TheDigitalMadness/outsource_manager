from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ResultsWay(StatesGroup):
    choose_action = State()


class Messages:
    results = (
        "За 2024-июль25 гг. по предварительным заданиям Заказчика продано товаров наших клиентов примерно на $5 млн. Из них в торг. сети около 75%.\n"
        "Портфель покупателей на июль 2025г: 4 торговые сети Беларуси, 2 торговые сети России, 1 площадка-маркетплейс России (входит в топ-3), 4 интернет-магазина Беларуси.\n"
        "Портфель налаженных коммуникаций (есть запросы от покупателя, нет соответствующего предложения от Производителя): все торговые сети Беларуси, около 10 торговых сетей России, 1 торговая сеть Узбекистана, порядка 60 оптовых покупателей в СНГ, 4 свободных торговых агента в Беларуси и России.\n"
        "Офис в Беларуси, Минск. План на 2026 год – открытие офиса в России, Москва.\n\n"
        "📌 Посмотрите короткие кейсы:"
    )


class Markups:
    choose_action = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔍 Смотреть все кейсы", callback_data="see_all_cases")],
            [InlineKeyboardButton(text="🎯 Оценить мой потенциал", callback_data="audit")],
            [InlineKeyboardButton(text="👤 Контакты для связи", callback_data="contacts")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
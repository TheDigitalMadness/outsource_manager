from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class WhatIsServiceWay(StatesGroup):
    choose_action = State()


class Messages:
    about = (
        "По заданию Заказчика Услуги «Вход» в одну из торговых сетей России или Беларуси.\n"
        "Подключаюсь к запросу (или даю обоснованный отказ) за 48 часов:\n"
        "• руководитель проекта\n"
        "• поиск вариантов актуальных сделок\n"
        "• оплата только за результат или фикс + % (на Ваш выбор)."
    )

    checklist = (
        "Предлагаемый чек-лист начала сотрудничества (возможна корректировка):\n"
        "1. Сбор и анализ информации о Ваших товарах, желаниях, задачах, возможностях\n"
        "2. Формулировка «основного запроса» - цели или списка целей\n"
        "3. Подготовка перечня наших предложений по достижению поставленных целей\n"
        "4. Совместно: проработка вариантов, выбор приоритетного варианта, «дорожная карта»\n"
        "5. Заключение договора о сотрудничестве\n"
        "6. Тестовый период\n"
        "7. Успех\n"
        "8. Масштабирование"
    )


class Markups:
    choose_action = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚙️ Как мы работаем", callback_data="how_we_work")],
            [InlineKeyboardButton(text="📝 Чек-лист «Начало продаж»", callback_data="send_start_pdf")],
            [InlineKeyboardButton(text="🆓 Бесплатный аудит", callback_data="audit")],
            [InlineKeyboardButton(text="👤 Контакты для связи", callback_data="contacts")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
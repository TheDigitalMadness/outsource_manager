from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class PricesWay(StatesGroup):
    choose_action = State()


class Messages:
    text = (
        "Тарифы прозрачны — платите либо за сделки, либо по фиксированному пакету. Ниже и далее указан ориентир, конкретику рассчитываю индивидуально и совместно решаем – что и по чем?\n\n"
        "🥉 Start — 0 ₽ фикс + 15 % с продаж\n"
        "🥈 Pro — $1000/мес + 10 % с продаж\n"
        "🥇 Dedicated — $2000/мес + 6,25 % с продаж\n"
        "🏆 your option number 1 – индивидуальная ценовая договоренность"
    )


class Markups:
    choose_action = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📆 Подробные расценки", callback_data="prices_pdf")],
            [InlineKeyboardButton(text="📝 Запросить расчёт для моего бизнеса", callback_data="audit")],
            [InlineKeyboardButton(text="👤 Контакты для связи", callback_data="contacts")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
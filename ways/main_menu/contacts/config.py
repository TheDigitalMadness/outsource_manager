from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ContactsWay(StatesGroup):
    choose_action = State()


class Messages:
    text = (
        "Вы можете связаться с нами в ТГ (@stm_himoza_cosmetika ), или по телефону (+79384964506), или по мессенджеру MAX (+79384964506) ."
    )


class Markups:
    choose_action = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
        ]
    )
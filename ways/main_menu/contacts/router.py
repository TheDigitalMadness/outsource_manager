from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

import ways.main_menu.contacts.config as cfg
import ways.main_menu.config as main_menu_cfg

import logging

router = Router()


@router.callback_query(main_menu_cfg.MainMenuWay.choose_action, F.data == "contacts")
async def open_contacts(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(cfg.Messages.text, reply_markup=cfg.Markups.choose_action)
    await state.set_state(cfg.ContactsWay.choose_action)


@router.callback_query(cfg.ContactsWay.choose_action, F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    logging.info(f"Going back from")
    await callback.message.edit_text(
        text=main_menu_cfg.Messages.greeting(callback.from_user.first_name or "друг"),
        reply_markup=main_menu_cfg.Markups.choose_action
    )
    await state.set_state(main_menu_cfg.MainMenuWay.choose_action)

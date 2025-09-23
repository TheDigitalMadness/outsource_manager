import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

import ways.main_menu.what_is_service.config as cfg
import ways.main_menu.config as main_menu_cfg
from ways.main_menu.contacts import config as contacts_cfg
import base_config.config as app_cfg

from ways.main_menu.audit import router as audit_router

router = Router()


@router.callback_query(cfg.WhatIsServiceWay.choose_action, F.data == "how_we_work")
async def how_we_work(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(cfg.Messages.checklist)
    # Кнопки остаются те же (по ТЗ)


@router.callback_query(cfg.WhatIsServiceWay.choose_action, F.data == "send_start_pdf")
async def send_start_pdf(callback: CallbackQuery, state: FSMContext):
    logging.log(logging.INFO, app_cfg.Files.START_SELL_PDF)
    await callback.message.answer_document(FSInputFile(app_cfg.Files.START_SELL_PDF))


@router.callback_query(main_menu_cfg.MainMenuWay.choose_action, F.data == "what_is_service")
async def open_service(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=cfg.Messages.about,
        reply_markup=cfg.Markups.choose_action
    )
    await state.set_state(cfg.WhatIsServiceWay.choose_action)


@router.callback_query(cfg.WhatIsServiceWay.choose_action, F.data == "audit")
async def go_audit(callback: CallbackQuery, state: FSMContext):
    await audit_router.start_audit(callback, state)


@router.callback_query(cfg.WhatIsServiceWay.choose_action, F.data == "contacts")
async def go_contacts(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(contacts_cfg.Messages.text, reply_markup=contacts_cfg.Markups.choose_action)
    await state.set_state(contacts_cfg.ContactsWay.choose_action)


@router.callback_query(cfg.WhatIsServiceWay.choose_action, F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=main_menu_cfg.Messages.greeting(callback.from_user.first_name or "друг"),
        reply_markup=main_menu_cfg.Markups.choose_action
    )
    await state.set_state(main_menu_cfg.MainMenuWay.choose_action)
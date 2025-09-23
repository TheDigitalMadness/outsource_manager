from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile

import ways.main_menu.results.config as cfg
import ways.main_menu.config as main_menu_cfg
from ways.main_menu.contacts import config as contacts_cfg
import ways.main_menu.audit.config as audit_cfg
import base_config.config as app_cfg

from ways.main_menu.audit import router as audit_router

router = Router()


@router.callback_query(main_menu_cfg.MainMenuWay.choose_action, F.data == "results")
async def open_results(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(cfg.Messages.results, reply_markup=cfg.Markups.choose_action)
    await state.set_state(cfg.ResultsWay.choose_action)


@router.callback_query(cfg.ResultsWay.choose_action, F.data == "see_all_cases")
async def send_all_cases(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer_document(FSInputFile(app_cfg.Files.CASES_XLSX))


@router.callback_query(cfg.ResultsWay.choose_action, F.data == "audit")
async def go_audit(callback: CallbackQuery, state: FSMContext):
    await audit_router.start_audit(callback, state)
    await state.set_state(audit_cfg.AuditWay.choose_action)


@router.callback_query(cfg.ResultsWay.choose_action, F.data == "contacts")
async def go_contacts(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(contacts_cfg.Messages.text, reply_markup=contacts_cfg.Markups.choose_action)
    await state.set_state(contacts_cfg.ContactsWay.choose_action)


@router.callback_query(cfg.ResultsWay.choose_action, F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=main_menu_cfg.Messages.greeting(callback.from_user.first_name or "друг"),
        reply_markup=main_menu_cfg.Markups.choose_action
    )
    await state.set_state(main_menu_cfg.MainMenuWay.choose_action)
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

import ways.main_menu.config as cfg

from ways.main_menu.contacts import config as contacts_cfg
from ways.main_menu.what_is_service import config as service_cfg
from ways.main_menu.refusal import config as refusal_cfg
from ways.main_menu.results import config as results_cfg
from ways.main_menu.prices import config as prices_cfg
from ways.main_menu.audit import config as audit_cfg

from ways.main_menu.audit import router as audit_router

from database.database import User

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    first_name = message.from_user.first_name or "друг"

    # Создаём пользователя в БД при первом старте, если нужен учёт
    if not User.get_by_tg_id(message.from_user.id):
        User.create_if_not_exists(tg_id=message.from_user.id, full_name=message.from_user.full_name or "")

    await message.answer(
        text=cfg.Messages.greeting(first_name),
        reply_markup=cfg.Markups.choose_action
    )
    await state.set_state(cfg.MainMenuWay.choose_action)


@router.callback_query(cfg.MainMenuWay.choose_action, F.data == "what_is_service")
async def open_service(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=service_cfg.Messages.about,
        reply_markup=service_cfg.Markups.choose_action
    )
    await state.set_state(service_cfg.WhatIsServiceWay.choose_action)


@router.callback_query(cfg.MainMenuWay.choose_action, F.data == "refusal")
async def open_refusal(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=refusal_cfg.Messages.text,
        reply_markup=refusal_cfg.Markups.choose_action
    )
    await state.set_state(refusal_cfg.RefusalWay.choose_action)


@router.callback_query(cfg.MainMenuWay.choose_action, F.data == "results")
async def open_results(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=results_cfg.Messages.results,
        reply_markup=results_cfg.Markups.choose_action
    )
    await state.set_state(results_cfg.ResultsWay.choose_action)


@router.callback_query(cfg.MainMenuWay.choose_action, F.data == "prices")
async def open_prices(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=prices_cfg.Messages.text,
        reply_markup=prices_cfg.Markups.choose_action
    )
    await state.set_state(prices_cfg.PricesWay.choose_action)


@router.callback_query(cfg.MainMenuWay.choose_action, F.data == "audit")
async def open_audit(callback: CallbackQuery, state: FSMContext):
    await audit_router.start_audit(callback, state)
    await state.set_state(audit_cfg.AuditWay.choose_action)

@router.callback_query(cfg.MainMenuWay.choose_action, F.data == "contacts")
async def open_contacts(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=contacts_cfg.Messages.text,
        reply_markup=contacts_cfg.Markups.choose_action
    )
    await state.set_state(contacts_cfg.ContactsWay.choose_action)
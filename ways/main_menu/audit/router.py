from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from datetime import datetime, timezone, timedelta

import ways.main_menu.audit.config as cfg
import ways.main_menu.config as main_menu_cfg
from ways.main_menu.contacts import config as contacts_cfg
from database.database import User

from base_config.config import TELEGRAM_BOT_TOKEN

bot = Bot(token=TELEGRAM_BOT_TOKEN)

router = Router()


async def start_audit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(cfg.Messages.steps[0], reply_markup=cfg.Markups.wizard)
    await state.update_data(audit_answers={})
    await state.set_state(cfg.AuditWay.q1)


# Обработчики текстовых ответов
@router.message(cfg.AuditWay.q1)
async def a_q1(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("audit_answers", {})
    answers["q1"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[1], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q2)


@router.message(cfg.AuditWay.q2)
async def a_q2(message: Message, state: FSMContext):
    data = await state.get_data(); answers = data.get("audit_answers", {})
    answers["q2"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[2], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q3)


@router.message(cfg.AuditWay.q3)
async def a_q3(message: Message, state: FSMContext):
    data = await state.get_data(); answers = data.get("audit_answers", {})
    answers["q3"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[3], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q4)


@router.message(cfg.AuditWay.q4)
async def a_q4(message: Message, state: FSMContext):
    data = await state.get_data(); answers = data.get("audit_answers", {})
    answers["q4"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[4], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q5)


@router.message(cfg.AuditWay.q5)
async def a_q5(message: Message, state: FSMContext):
    data = await state.get_data(); answers = data.get("audit_answers", {})
    answers["q5"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[5], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q6)


@router.message(cfg.AuditWay.q6)
async def a_q6(message: Message, state: FSMContext):
    data = await state.get_data(); answers = data.get("audit_answers", {})
    answers["q6"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[6], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q7)


@router.message(cfg.AuditWay.q7)
async def a_q7(message: Message, state: FSMContext):
    data = await state.get_data(); answers = data.get("audit_answers", {})
    answers["q7"] = message.text
    await state.update_data(audit_answers=answers)
    await message.answer(cfg.Messages.steps[7], reply_markup=cfg.Markups.wizard)
    await state.set_state(cfg.AuditWay.q8)

@router.message(cfg.AuditWay.q8)
async def a_q8(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data.get("audit_answers", {})
    answers["q8"] = message.text
    await state.update_data(audit_answers=answers)

    # Отправка итоговых сообщений
    await message.answer(cfg.Messages.done)

    # Возврат кнопок стартового меню
    import ways.main_menu.config as mm_cfg
    await message.answer(
        text=mm_cfg.Messages.greeting(message.from_user.first_name or "друг"),
        reply_markup=mm_cfg.Markups.choose_action
    )
    await state.set_state(mm_cfg.MainMenuWay.choose_action)

    # Рассылка заявки всем администраторам
    await notify_admins(message, state)

async def notify_admins(message: Message, state: FSMContext):
    # МСК время
    msk_now = datetime.now(timezone(timedelta(hours=3)))
    msk_str = msk_now.strftime("%H:%M %d.%m.%Y (МСК)")

    from_user = message.from_user
    username = f"@{from_user.username}" if from_user.username else ""

    data = await state.get_data()
    answers = data.get("audit_answers", {})

    text = (
        "Новая заявка!\n"
        f"Пользователь: {username}\n"
        f"Время заполнения заявки: {msk_str}\n"
        f"Название предприятия: {answers.get('q1','')}\n"
        f"ИНН/УНП: {answers.get('q2','')}\n"
        f"Сайт: {answers.get('q3','')}\n"
        f"Особенности: {answers.get('q4','')}\n"
        f"Запрос: {answers.get('q5','')}\n"
        f"Возможности: {answers.get('q6','')}\n"
        f"Телефон: {answers.get('q7','')}\n"
        f"Когда связаться: {answers.get('q8','')}"
    )

    admins = [u for u in User.get_all_users() if u.admin]
    # Включаем корневого админа обязательно
    root_id = 5379507619
    # 291803193
    admin_ids = {root_id} | {a.tg_id for a in admins}

    for admin_id in admin_ids:
        try:
            await bot.send_message(admin_id, text)
        except Exception as e:
            pass


# Обработчики кнопок Назад и Контакты в визарде
@router.callback_query(
    (
        cfg.AuditWay.choose_action | cfg.AuditWay.q1 | cfg.AuditWay.q2 | cfg.AuditWay.q3 | cfg.AuditWay.q4 | cfg.AuditWay.q5 | cfg.AuditWay.q6 | cfg.AuditWay.q7 | cfg.AuditWay.q8
    ),
    F.data == "back"
)
async def wizard_back(callback: CallbackQuery, state: FSMContext):
    # Определяем текущий шаг
    current = await state.get_state()
    order = [
        cfg.AuditWay.q1, cfg.AuditWay.q2, cfg.AuditWay.q3, cfg.AuditWay.q4,
        cfg.AuditWay.q5, cfg.AuditWay.q6, cfg.AuditWay.q7, cfg.AuditWay.q8
    ]
    if current in [s.state for s in order]:
        idx = [s.state for s in order].index(current)
        if idx > 0:
            prev_state = order[idx - 1]
            await state.set_state(prev_state)
            await callback.message.answer(cfg.Messages.steps[idx - 1], reply_markup=cfg.Markups.wizard)
        else:
            # Если это первый вопрос — возврат в главное меню
            await callback.message.answer(
            text=main_menu_cfg.Messages.greeting(callback.from_user.first_name or "друг"),
            reply_markup=main_menu_cfg.Markups.choose_action
            )
            await state.set_state(main_menu_cfg.MainMenuWay.choose_action)


@router.callback_query(
    (
            cfg.AuditWay.choose_action | cfg.AuditWay.q1 | cfg.AuditWay.q2 | cfg.AuditWay.q3 | cfg.AuditWay.q4 | cfg.AuditWay.q5 | cfg.AuditWay.q6 | cfg.AuditWay.q7 | cfg.AuditWay.q8
    ),
    F.data == "contacts"
)
async def wizard_contacts(callback: CallbackQuery, state: FSMContext):
    # Сброс визарда и переход в Контакты
    await state.clear()
    await callback.message.edit_text(contacts_cfg.Messages.text, reply_markup=contacts_cfg.Markups.choose_action)
    await state.set_state(contacts_cfg.ContactsWay.choose_action)
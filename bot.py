import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from base_config import config as app_cfg
from database.database import Database, User

# --- Логирование во внешний файл ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Бот и диспетчер ---
bot = Bot(token=app_cfg.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())


# Регистрация команд
async def set_bot_commands():
    commands = [
        BotCommand(command="help", description="Помощь по командам администрирования"),
        BotCommand(command="whitelist", description="Список администраторов"),
        BotCommand(command="adduser", description="Добавить администратора по TG ID"),
        BotCommand(command="deluser", description="Удалить администратора по TG ID"),
        BotCommand(command="start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands)

# --- Админ-команды ---
from aiogram.filters import Command
from aiogram.types import Message


def is_admin(tg_id: int) -> bool:
    if tg_id == app_cfg.ROOT_ADMIN_TG_ID:
        return True
    user = User.get_by_tg_id(tg_id)
    return bool(user and user.admin)


@dp.message(Command("help"))
async def help_cmd(message: Message):
    text = (
        "Функции для управления ботом:\n"
        "/adduser TG_ID – добавляет администратора по Telegram ID.\n"
        "/deluser TG_ID – удаляет администратора по Telegram ID.\n"
        "/whitelist – просмотр текущих администраторов.\n\n"
        "Telegram ID можно узнать с помощью бота @username_to_id_bot"
    )
    await message.answer(text)


@dp.message(Command("whitelist"))
async def whitelist_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    admins = [u for u in User.get_all_users() if u.admin]
    lines = [f"• {a.tg_id} — {a.full_name}" for a in admins]
    text = "Текущие администраторы:\n" + ("\n".join(lines) if lines else "— пусто —")
    await message.answer(text)


@dp.message(Command("adduser"))
async def adduser_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /adduser TG_ID")
        return
    target_id = int(parts[1])
    if not User.get_by_tg_id(target_id):
        User.create_if_not_exists(tg_id=target_id, full_name="")
    User.appoint_admin(target_id)
    await message.answer(f"Добавлен администратор: {target_id}")


@dp.message(Command("deluser"))
async def deluser_cmd(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("Использование: /deluser TG_ID")
        return
    target_id = int(parts[1])
    # снимаем права, но не удаляем из users
    from sqlite3 import connect
    conn = connect(Database.database_src)
    c = conn.cursor()
    c.execute("UPDATE users SET admin = 0 WHERE tg_id = ?", (target_id,))
    conn.commit(); conn.close()
    await message.answer(f"Удалён из администраторов: {target_id}")


@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery, state: FSMContext):
    logger.info("=== BACK PRESSED ===", await state.get_state())



# --- Регистрация всех роутеров ---
from ways.main_menu import router as main_menu_router
from ways.main_menu.what_is_service import router as what_router
from ways.main_menu.refusal import router as refusal_router
from ways.main_menu.results import router as results_router
from ways.main_menu.prices import router as prices_router
from ways.main_menu.audit import router as audit_router
from ways.main_menu.contacts import router as contacts_router


dp.include_router(main_menu_router.router)
dp.include_router(what_router.router)
dp.include_router(refusal_router.router)
dp.include_router(results_router.router)
dp.include_router(prices_router.router)
dp.include_router(audit_router.router)
dp.include_router(contacts_router.router)


async def on_startup():
    Database.database_src = "database/database.db"
    Database.init_db()
    await set_bot_commands()
    logger.info("Bot started")


async def main():
    await on_startup()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
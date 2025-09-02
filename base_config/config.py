# config.py
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

# Загрузи TOKEN из .env или переменных окружения любым способом, который ты используешь у себя
# Здесь для простоты просто читаем переменную окружения

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "CHANGE_ME")

# TG ID кодового администратора
ROOT_ADMIN_TG_ID = 5379507619
# 291803193

# Часовой пояс по ТЗ — московский (UTC+3)
MOSCOW_TZ = "+03:00"

# Пути к файлам, которые лежат на сервере
BASE_FILES_DIR = os.getenv("FILES_DIR", os.path.abspath("files"))

@dataclass
class Files:
    CASES_XLSX: str = os.path.join(BASE_FILES_DIR, "Кейсы.xlsx")
    PRICES_PDF: str = os.path.join(BASE_FILES_DIR, "Расценки.pdf")
    START_SELL_PDF: str = os.path.join(BASE_FILES_DIR, "Начало продаж в торговую сеть.pdf")
    CASES_PDFS: tuple = (
        os.path.join(BASE_FILES_DIR, "Кейс 1.pdf"),
        os.path.join(BASE_FILES_DIR, "Кейс 2.pdf"),
        os.path.join(BASE_FILES_DIR, "Кейс 3.pdf"),
        os.path.join(BASE_FILES_DIR, "Кейс 4.pdf"),
        os.path.join(BASE_FILES_DIR, "Кейс 5.pdf"),
    )
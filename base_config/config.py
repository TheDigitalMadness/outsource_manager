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
    CASES_XLSX: str = os.path.join(BASE_FILES_DIR, "cases.xlsx")
    PRICES_PDF: str = os.path.join(BASE_FILES_DIR, "prices.pdf")
    START_SELL_PDF: str = os.path.join(BASE_FILES_DIR, "sell_starting_in_sellers_network.pdf")
    CASES_PDFS: tuple = (
        os.path.join(BASE_FILES_DIR, "case1.pdf"),
        os.path.join(BASE_FILES_DIR, "case2.pdf"),
        os.path.join(BASE_FILES_DIR, "case3.pdf"),
        os.path.join(BASE_FILES_DIR, "case4.pdf"),
        os.path.join(BASE_FILES_DIR, "case5.pdf"),
    )
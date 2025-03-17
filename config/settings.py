"""
Конфигурационный файл для приложения по сбору метрик и отправке их в Google Sheets
"""

import os
from pathlib import Path

# Базовые пути
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"

# Параметры для авторизации в Google Sheets
GOOGLE_SERVICE_FILE = str(CONFIG_DIR / "striking-domain.json")  # Путь к файлу авторизации сервисного аккаунта
SHEET_NAME = os.getenv("SHEET_NAME", "YOUR_SHEET_NAME")  # Название таблицы
SHEET_KEY = os.getenv("SHEET_KEY", "YOUR_SHEET_KEY")  # Ключ таблицы
WORKSHEET_NAME = os.getenv("WORKSHEET_NAME", "YOUR_WORKSHEET_NAME")  # Название листа

# Параметры для API Astromkey
ASTROMKEY_API = {
    "headers": {
        "accept": "application/json; charset=utf-8",
        "Authorization": os.getenv("ASTROMKEY_API_TOKEN", "YOUR_API_TOKEN")
    },
    "base_url": os.getenv("ASTROMKEY_API_URL", "YOUR_API_BASE_URL")
}

# Параметры времени для сбора метрик
METRICS_TIME_CONFIG = {
    "from_time": "-24h",  # Период сбора метрик (от)
    "to_time": "now",     # Период сбора метрик (до)
    "execution_hour": int(os.getenv("EXECUTION_HOUR", "23")),  # Час выполнения скрипта
    "execution_minute": int(os.getenv("EXECUTION_MINUTE", "0"))  # Минута выполнения скрипта
}

# Параметры логирования
LOG_FILE_PATH = str(BASE_DIR / "logs" / "watchdog.log")  # Путь к файлу логов 
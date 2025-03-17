"""
Основной модуль приложения для сбора метрик из Astromkey и отправки их в Google Sheets.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import requests
import json
import pygsheets
from datetime import date, datetime
import time
import numpy as np
import logging
from config.settings import (
    GOOGLE_SERVICE_FILE,
    SHEET_NAME,
    SHEET_KEY,
    WORKSHEET_NAME,
    ASTROMKEY_API,
    METRICS_TIME_CONFIG,
    LOG_FILE_PATH,
)

# Инициализация подключения к Google Sheets
gc = pygsheets.authorize(service_file=GOOGLE_SERVICE_FILE)
sheet = gc.open_by_key(SHEET_KEY)
wSheet = sheet.worksheet_by_title(WORKSHEET_NAME)

# Загрузка метрик из конфигурационного файла
with open(Path(__file__).parent.parent / "config" / "metrics.json", "r") as json_file:
    metric_data = json.load(json_file)

def extract_values(data, key):
    """
    Рекурсивная функция для извлечения всех значений по ключу в JSON-структуре.
    
    Args:
        data: JSON-структура для поиска
        key: Ключ для поиска значений
    
    Returns:
        list: Список найденных значений
    """
    result = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                result.append(v)
            elif isinstance(v, (dict, list)):
                result.extend(extract_values(v, key))
    elif isinstance(data, list):
        for item in data:
            result.extend(extract_values(item, key))
    return result

def collect_metrics(metric, entity):
    """
    Функция сбора метрик из Astromkey с фильтрацией и усреднением данных.
    
    Args:
        metric (str): Селектор метрики
        entity (str): ID сущности или 'empty' если не требуется
    
    Returns:
        float: Усредненное значение метрики
    """
    if entity == "empty":
        params = {
            "metricSelector": metric,
            "from": METRICS_TIME_CONFIG["from_time"],
            "to": METRICS_TIME_CONFIG["to_time"],
        }
    else:
        params = {
            "metricSelector": metric,
            "from": METRICS_TIME_CONFIG["from_time"],
            "to": METRICS_TIME_CONFIG["to_time"],
            "entitySelector": f"entityId({entity})",
        }

    try:
        response = requests.get(
            ASTROMKEY_API["base_url"],
            params=params,
            headers=ASTROMKEY_API["headers"],
        )
        data = response.json()

    except requests.exceptions.RequestException as err:
        print(f"Ошибка: {err}")
        return None

    value = extract_values(data, "values")
    filtered_value = [item for sublist in value for item in sublist if item is not None]
    
    if not filtered_value:
        return None
        
    avgValue = sum(filtered_value) / len(filtered_value)
    
    # Нормализация значений в зависимости от типа метрики
    if any(word in metric for word in ["builtin:service.", "calc:service."]):
        avgValue /= 1000000
    elif any(word in metric for word in ["builtin:apps.", "uacm."]):
        avgValue /= 1000

    return avgValue

def check_sheet_date():
    """
    Проверяет и возвращает номер столбца для текущей даты.
    
    Returns:
        int: Номер столбца с текущей датой
    """
    today = date.today().strftime("%m/%d/%Y")
    try:
        findDateCol = wSheet.find(today)
        return findDateCol[0].col
    except Exception as err:
        print(f"Ошибка при поиске даты: {err}")
        return None

def update_sheet_values(metricName, metricValue):
    """
    Обновляет значения в таблице Google Sheets.
    
    Args:
        metricName (str): Название метрики
        metricValue (float): Значение метрики
    """
    try:
        findMetricRow = wSheet.find(metricName)
        col = check_sheet_date()
        if col:
            wSheet.update_value((findMetricRow[0].row, col), metricValue)
    except Exception as err:
        print(f"Ошибка при обновлении значений: {err}")

def check_time():
    """
    Проверяет, наступило ли время выполнения скрипта.
    
    Returns:
        bool: True если текущее время соответствует заданному времени выполнения
    """
    current_time = datetime.now().time()
    return (current_time.hour == METRICS_TIME_CONFIG["execution_hour"] and 
            current_time.minute == METRICS_TIME_CONFIG["execution_minute"])

def setup_logger(log_file_path=LOG_FILE_PATH):
    """
    Настраивает и возвращает логгер.
    
    Args:
        log_file_path (str): Путь к файлу логов
    
    Returns:
        logging.Logger: Настроенный объект логгера
    """
    logger = logging.getLogger("script_logger")
    logger.setLevel(logging.DEBUG)
    
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

def log_message(logger, message):
    """
    Записывает сообщение в лог.
    
    Args:
        logger (logging.Logger): Объект логгера
        message (str): Сообщение для записи
    """
    logger.info(message)

def main():
    """
    Основная функция приложения.
    Запускает бесконечный цикл сбора и записи метрик по расписанию.
    """
    logger = setup_logger()
    log_message(logger, "Script was running")
    
    try:
        while True:
            if check_time():
                for metric in metric_data["metrics"]:
                    mValue = collect_metrics(metric[1], metric[2])
                    if mValue is not None:
                        print(f"{metric[3]}: {mValue}")
                        update_sheet_values(metric[0], mValue)
                log_message(logger, "Metrics wrote in the table!!! Good night")
            time.sleep(10)
    except Exception as e:
        log_message(logger, f"Exception: {e}")
    finally:
        log_message(logger, "Script was stopped")

if __name__ == "__main__":
    main() 
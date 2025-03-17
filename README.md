# Ключ-АСТРОМ to Google Sheets Metrics Exporter

Приложение для автоматического сбора метрик из Ключ-АСТРОМ и экспорта их в Google Sheets.

## Описание

Это приложение автоматически собирает метрики из Ключ-АСТРОМ API и экспортирует их в Google Sheets таблицу. Приложение работает по расписанию, собирая данные в заданное время и обновляя соответствующие ячейки в таблице.

## Структура проекта

```
.
├── src/                    # Исходный код приложения
│   ├── __init__.py
│   └── main.py            # Основной модуль приложения
├── config/                 # Конфигурационные файлы
│   ├── __init__.py
│   ├── settings.py        # Основные настройки
│   ├── metrics.json       # Конфигурация метрик
│   └── striking-domain.json # Файл авторизации Google (не включен в репозиторий)
├── logs/                   # Директория для логов
│   └── watchdog.log
├── .env.example           # Пример файла с переменными окружения
├── requirements.txt        # Зависимости проекта
├── Dockerfile             # Конфигурация Docker
└── docker-compose.yml     # Конфигурация Docker Compose
```

## Требования

- Python 3.8+
- Docker и Docker Compose (для запуска в контейнере)
- Доступ к Ключ-АСТРОМ API
- Сервисный аккаунт Google Sheets с соответствующими разрешениями

## Конфигурация

### Переменные окружения

Создайте файл `.env` на основе `.env.example` и заполните следующие переменные:

```bash
# Google Sheets configuration
SHEET_NAME=YOUR_SHEET_NAME          # Название таблицы
SHEET_KEY=YOUR_SHEET_KEY           # Ключ таблицы
WORKSHEET_NAME=YOUR_WORKSHEET_NAME  # Название листа

# Astromkey API configuration
ASTROMKEY_API_TOKEN=YOUR_API_TOKEN  # Токен API Ключ-АСТРОМ
ASTROMKEY_API_URL=YOUR_API_BASE_URL # URL API Ключ-АСТРОМ

# Execution schedule
EXECUTION_HOUR=23                   # Час выполнения (0-23)
EXECUTION_MINUTE=0                  # Минута выполнения (0-59)
```

### Файлы конфигурации

1. `config/settings.py` - основные настройки приложения:

   - Параметры подключения к Google Sheets
   - Настройки API Ключ-АСТРОМ
   - Параметры времени выполнения
   - Настройки логирования

2. `config/metrics.json` - конфигурация метрик для сбора:

   ```json
   {
     "metrics": [["Имя метрики", "Селектор метрики", "ID сущности", "Описание"]]
   }
   ```

3. `config/striking-domain.json` - файл авторизации сервисного аккаунта Google (необходимо создать отдельно)

## Установка и запуск

### Локальный запуск

1. Клонируйте репозиторий:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

3. Настройте конфигурационные файлы:

   - Создайте файл `.env` на основе `.env.example` и заполните необходимые переменные
   - Добавьте файл авторизации Google (`config/striking-domain.json`)
   - Создайте файл `config/metrics.json` с нужными метриками

4. Запустите приложение:
   ```bash
   python src/main.py
   ```

### Запуск в Docker

1. Настройте переменные окружения:

   ```bash
   cp .env.example .env
   # Отредактируйте файл .env, установив необходимые значения
   ```

2. Соберите и запустите контейнер:
   ```bash
   docker-compose up -d
   ```

## Логирование

Приложение ведет логи в файл `logs/watchdog.log`, записывая информацию о:

- Запуске и остановке скрипта
- Успешной записи метрик
- Ошибках во время выполнения

## Безопасность

- Храните конфиденциальные данные в файле `.env` (не включен в репозиторий)
- Не публикуйте файл `.env` или `striking-domain.json` в репозитории
- В production используйте безопасные способы передачи секретов (например, Docker secrets или Kubernetes secrets)

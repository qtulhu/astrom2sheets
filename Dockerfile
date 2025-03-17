FROM python:3.8-slim

WORKDIR /app

# Копируем только requirements.txt сначала для использования кэша Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаем необходимые директории
RUN mkdir -p logs config

# Копируем файлы проекта
COPY src/ ./src/
COPY config/ ./config/

# Создаем файл с переменными окружения по умолчанию
COPY .env.example .env

# Запускаем приложение
CMD ["python", "src/main.py"] 
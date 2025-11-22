# Этап 1: сборка (опционально, но для продакшена — да)
FROM python:3.11-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Этап 2: финальный образ
FROM python:3.11-slim

# Установка зависимостей ОС (если нужны: например, для Pillow)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только нужное (исключаем .git, venv и т.д.)
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH

# Порт Django
EXPOSE 8000

# Запуск
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
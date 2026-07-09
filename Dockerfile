# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной проект
COPY . .

# Команда для запуска (будет переопределена в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# Используем официальный образ Python как базовый
FROM python:3.9-slim
# Устанавливаем рабочую директорию в контейнере
WORKDIR /app
# Копируем файлы зависимостей
COPY ../requirements.txt .
# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
# Копируем все файлы проекта в контейнер
COPY . .
# Указываем порт, который будет использоваться приложением
EXPOSE 8000
# Команда для запуска приложения
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
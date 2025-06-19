FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости отдельно для кэширования
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы при запуске через volumes
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8190", "--reload"]
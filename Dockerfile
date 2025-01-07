# Використовуємо базовий образ Python 3.12
FROM python:3.12-slim

# Встановлюємо необхідні системні пакети
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    libmariadb-dev \
    libmariadb-dev-compat \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли проекту
COPY . /app

# Встановлюємо Python-залежності
RUN pip install --no-cache-dir -r requirements.txt

# Запускаємо основний скрипт
CMD ["python", "main.py"]

# Используем базовый образ Python
FROM python:3.10

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Копируем зависимости в контейнер
COPY ./requirements.txt /code/

# Устанавливаем зависимости
RUN pip install -r /code/requirements.txt

# Копируем код приложения в контейнер
COPY . .

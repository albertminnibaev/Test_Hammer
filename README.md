# Сервис для реферальной системы
1. Перед началом работы в корне проекта необходимо создать файл .env для хранения переменных окружения.
Файл .env создается на основе файла .env.sample.
Файл .env содержит следующие переменные:
   * SECRET_KEY - секретный ключ Django;
   * PASSWORD_DATABASE - пароль для подключения к базе данных;
   * POSTGRES_DB - имя при подключении к базе данных при помощи Docker-Compose (postgres);
   * POSTGRES_USER - имя при подключении к базе данных при помощи Docker-Compose (postgres);
   * POSTGRES_PASSWORD - пароль при подключении к базе данных при помощи Docker-Compose;
   * PGDATA - при подключении к базе данных при помощи Docker-Compos (/var/lib/postgresql/data/pgdata);
   * EMAIL - логин в сервисе SMS Aero;
   * SMS_KEY - секретный ключ SMS Aero;

2. Для регистрации и аутентификации используется стандартные инструменты Django REST framework с использованием библиотеку djangorestframework-simplejwt
3. Для запуска проекта необходимо запустить само приложение коммандой - python manage.py runserver
4. Для запуска проекта при помощи Docker-Compose необходимо в файле settings.py активировать соответствующие настройки
5. В проекте реализована отправка кода авторизации на номер телефона пользователя через сервис SMS Aero. (код закоментирован)

## Описание документации к API:
Для автоматической регистрации используются Swagger и Redoc.
Пример основных запросов:
1. Запрос на получение 4х значного кода при регистрация пользователя:


    запрос POST user/veryfi/
    параметры запроса
    {
       "phone": "+79999999999"
    }

    ответ: 

    статус код: 200 OK

    {
      "message": "Code created successfully"
    }

2. Регистрация пользователя как реферала:


    запрос POST user/auth/
    параметры запроса
    {
      "phone": "+79999999999",
      "otp_code": "1234"
    }

    ответ: 

    статус код: 200 OK

    {
      "access_token": "access_token",
      "refresh_token": "refresh_token"
    }

3. Получение информации о пользователе:


    запрос GET users/{id}/

    ответ: 

    статус код: 200 OK

    {
       "phone": "+79999999999",
       "first_name": "string",
       "last_name": "string",
       "referral_code": 1234,
       "referral_code_refer": 1234,
       "refer": 1,
       "referral_list": ["+79999999999", "+79999999999", "+79999999999"]
    }

4. Создание запроса на ввод чужого реферального ключа:


    запрос POST users/refer/
    параметры запроса
    {
       "referral_code": "jqpQZf"
    }

    ответ: 

    статус код: 200 OK

    {
      "referral_code_refer": "string",
      "refer": "string"
    }

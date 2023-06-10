![Python](https://img.shields.io/badge/-Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/-Django-092E20?style=flat&logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/-Django_REST_Framework-FF1709?style=flat&logo=django&logoColor=white)

# API приложения знакомств

Это RESTful API для приложения знакомств. Он позволяет пользователям создавать аккаунты, просматривать других пользователей и находить совпадения на основе взаимного интереса. API предоставляет эндпоинты для регистрации пользователей, просмотра списка пользователей и функциональности совпадений.

## Возможности

- Регистрация пользователя: Пользователи могут создавать аккаунты, указывая свои данные, включая имя пользователя, пароль, аватар, имя, пол, электронную почту, широту и долготу.
- Список пользователей: Пользователи могут просматривать список других пользователей, отфильтрованный по полу, имени и фамилии, а также дополнительно по расстоянию от их местоположения.
- Совпадения: Пользователи могут выразить свою заинтересованность в других пользователях, создавая взаимные совпадения.

## Используемые технологии

- Django: Веб-фреймворк для создания API.
- Django REST Framework: Набор инструментов для создания веб-API с помощью Django.
- PIL: Библиотека для обработки аватаров пользователей.
- Django Filter: Обеспечивает возможности фильтрации для представлений Django.
- Django REST Framework Filters: Добавляет поддержку фильтрации для Django REST Framework.
- Django REST Framework JWT: Аутентификация на основе токенов JSON Web.
- Django REST Framework Swagger: Генератор документации для API.
- PostgreSQL: Реляционная база данных для хранения данных пользователей.

## Начало работы

Чтобы начать работу с проектом, выполните следующие шаги:

1. Клонируйте репозиторий:

   ```
   git clone https://github.com/your-username/dating-app-api.git
   ```

2. Перейдите в директорию проекта:

    ```
    cd dating-app-api
    ```

3. Установите зависимости:

    ```
    pip install -r requirements.txt
    ```

4. Настройте базу данных:

    Создайте базу данных PostgreSQL для проекта.

    Обновите конфигурацию базы данных в файле settings.py.

    ```
    DB_ENGINE: Движок базы данных, используемый Django.
    DB_NAME: Название базы данных, которая будет создана или используется для проекта.
    POSTGRES_USER: Имя пользователя для подключения к базе данных PostgreSQL.
    POSTGRES_PASSWORD: Пароль пользователя для подключения к базе данных PostgreSQL.
    DB_HOST: Хост базы данных, где запущен PostgreSQL.
    DB_PORT: Порт базы данных PostgreSQL.
    ```

    Пример:
    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=dating_db
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password
    DB_HOST=localhost
    DB_PORT=5432
    ```

    Выполните миграции базы данных:

    ```
    python manage.py migrate
    ```

5. Настройте сервер почтового клиента для отправки писем в файле settings.py.
    ```
    EMAIL_BACKEND: Бэкэнд электронной почты, используемый Django.
    EMAIL_HOST: SMTP-сервер, через который будет осуществляться отправка электронных сообщений.
    EMAIL_PORT: Порт, используемый для подключения к SMTP-серверу. В данном случае указан порт 2525.
    EMAIL_HOST_USER: Имя пользователя для аутентификации на SMTP-сервере.
    EMAIL_HOST_PASSWORD: Пароль пользователя для аутентификации на SMTP-сервере.
    EMAIL_USE_TLS: Флаг, указывающий на использование TLS (Transport Layer Security) для безопасной передачи данных между приложением и SMTP-сервером.
    EMAIL_USE_SSL: Флаг, указывающий на использование SSL (Secure Sockets Layer) для безопасной передачи данных.
    SERVER_EMAIL: Адрес электронной почты, который будет использоваться как адрес отправителя для системных сообщений или ошибок.
    DEFAULT_FROM_EMAIL: Адрес электронной почты, который будет использоваться как адрес отправителя по умолчанию для всех электронных сообщений.
    ```

    Пример:
    ```
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.mail.ru'
    EMAIL_PORT = 2525
    EMAIL_HOST_USER = `user@mail.ru`
    EMAIL_HOST_PASSWORD = `password`
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    SERVER_EMAIL = EMAIL_HOST_USER
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
    ```

6. Запустите сервер разработки:

    ```
    python manage.py runserver
    ```

7. Доступ к API будет доступен по адресу `http://localhost:8000/api/`

# api_yamdb
api_yamdb
Учебный проект API от Яндекс.Практикум на DjangoRestFramework

## Авторы
команда 

## Технологии
такие-то такие-то

### Установка: 
#### Windows
`python -m venv venv `

`venv/Scripts/activate `

`python -m pip install --upgrade pip `

`pip install -r requirements.txt `

#### Linux
`python3 -m venv venv `

`source venv/bin/activate `

`python -m pip install --upgrade pip `

`pip install --upgrade setuptools ` опционально...

`python -m pip install --upgrade pip setuptools` либо так)

`pip install -r requirements.txt `

### Запуск
Перейдити в дирректорию api_yamdb и выполните миграции:

`python manage.py migrate `

Запустите сервер:

`python manage.py runserver`

## Функционал
## позже надо бы изменить...
Как проверить работоспособность:
создаем суперюзера
`python3 manage.py createsuperuser`

запускаем сервер
`python3 manage.py runserver`

через post запрос получаем токен пользователя:
`/api/v1/jwt/create/`

в body запроса передаем наши пароль и логин:
**{
"username": "string",
"password": "string"
}**

полученный токен передаем в header запроса.

Неавторизованные пользователи имеют доступ только на чтение:

`GET api/v1/posts/ - получить список всех постов`

`GET api/v1/posts/{id}/ - получение поста по id`

`GET api/v1/groups/ - получение списка доступных групп`

`GET api/v1/groups/{id}/ - получение информации о конкретной группе по id`

`GET api/v1/{post_id}/comments/ - получение всех комментариев к посту`

`GET api/v1/{post_id}/comments/{id}/ - получение комментария к посту по id`


Подробные возможности можно увидеть после запуска сервера по ссылке:

`http://127.0.0.1:8000/redoc`


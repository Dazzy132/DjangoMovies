# Django Movies - Сайт Кинотеки  

--------------------------------------------------------

![Изображение Сайте](readme_images/chrome_wyuA5fzKwR.jpg)
![Фильмы](readme_images/img.png)

## 📄 Описание проекта

Проект представляет собой онлайн-базу фильмов с возможностью оставлять отзывы и оценки к ним. Пользователи могут искать фильмы по жанру, году выпуска, рейтингу. Также они могут оставлять отзывы и оценки к просмотренным фильмам, чтобы помочь другим пользователям сделать правильный выбор перед просмотром.

Регистрация на сайте сделана через библиотеку allauth. Так же подключена регистрация через VK (ВКонтакте).

На сайте доступна смена основного языка через библиотеку django-modeltranslation.

--------------------------------------------------------


## 🔧 Инструменты разработки:


[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

### Технологический стек (Backend):
- Python - 3.7
- Django - 3.2
- Django-modeltranslation (gettext)


-----------------------------------------------------------

### Наполнение .env-файла

Должен находиться в djangoProject1
```dotenv
SECRET_KEY="your-secret-key"
DB_ENGINE=django.db.backends.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-example.com
```

-------------------

# Как запустить проект

1) Клонировать репозиторий
```shell
git clone git@github.com:Dazzy132/DjangoMovies.git
```

2) Создать и активировать виртуальное окружение
```shell
python -m venv venv

source venv/Scripts/activate (Для Windows)
source venv/bin/activate (Для Linux и MacOS)
```
3)  Установить зависимости
```shell
pip install -r requirements.txt
```
4) Выполнить миграции
```shell
python manage.py makemigrations
python manage.py migrate
```
5) Создать суперпользователя (Рекомендуется)
```shell
python manage.py createsuperuser --username=root --email=root@mail.ru
```

6) Запустить сервер
```shell
python manage.py runserver
```
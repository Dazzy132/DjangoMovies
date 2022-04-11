from modeltranslation.translator import register, TranslationOptions
# Подключение мультиязычности для моделей
from .models import Category, Actor, Movie, Genre, MovieShots


# Регистрируем модель для перевода
# Создаём класс и наследуемся от TranslationOptions
# Указываем поля которые будут участвовать в переводе


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Actor)
class ActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(MovieShots)
class MovieShotsTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

# settings.py
#          INSTALLED_APPS = [
#               'modeltranslation',  # Мультиязычность - pip install django-modeltranslation
#           ]
#
#           MIDDLEWARE = [
#               'django.middleware.locale.LocaleMiddleware'     # Мультиязычность
#           ]
#
#           USE_I18N = True     # Проверяем True ли. Для мультиязычности
#
#           # Для мультиязычности. Делаем функцию лямбда. И кортежем передаем языки, на которых будет работать мультиязычность
#           gettext = lambda s: s
#           LANGUAGES = (
#               ('ru', gettext('Russia')),
#               ('en', gettext('English')),
#           )
#
#           LOCALE_PATHS = (
#                os.path.join(BASE_DIR, 'locale'),
#           )

# В этом файле создаем классы, где указываем те поля моделей, которые будут участвовать в переводе.
# После указания полей - python manage.py makemigrations и python manage.py migrate
# Если проект был только что создан. То ничего делать не надо. Если же уже есть поля, то их нужно синхронизировать
# Команда для синхронизации - python manage.py update_translation_fields
# Далее в Админке импортируем TranslationAdmin и наследуемся от него во всех моделях
# Переводим все что надо
# Делаем форму для переключения языка в _header

# {% load i18n }

#            <li>
#                {% comment %} Форма для перевода динамического.{% endcomment %}
#                <form action="{% url 'set_language' %}" method="post">{% csrf_token %}
#                    <input name="next" type="hidden" value="{{ redirect_to }}">
#                    <select name="language">
#                        {% get_current_language as LANGUAGE_CODE %}
#                        {% get_available_languages as LANGUAGES %}
#                        {% get_language_info_list for LANGUAGES as languages %}
#                        {% for language in languages %}
#                            <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %}
#                                    selected{% endif %}>
#                                {{ language.name_local }} ({{ language.code }})
#                            </option>
#                        {% endfor %}
#                    </select>
#                    <input type="submit" value="Go">
#                </form>
#            </li>


# Эта форма для перевода динамических данных. Для статических данных - в нужных местах указываем
# {% load i18n %}
# {% trans 'Год' %}
#  пишем django-admin makemessages -l en -e html
# В locale создается / en / LC_MESSAGES / django.po
# Указываем перевод для слов
# Как указали перевод - django-admin compilemessages
# Создается файл django.mo


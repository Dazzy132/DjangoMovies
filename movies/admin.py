from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


#
class ReviewInline(admin.TabularInline):   # admin.StackedInline
    """Отзывы на странице фильма"""
    model = Reviews
    # Модель, которая используется
    extra = 1
    # Дополнительные поля для заполнения
    readonly_fields = ("name", "email")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    prepopulated_fields = {"url": ("title",)}
    # Делать поле url на основе поля title. Автозаполнение
    search_fields = ("title", "category__name")
    # Поиск по имени категории, через обращение к БД
    inlines = [ReviewInline]
    # inlines - Для MTM FRK. Прикрепление классов к таблице
    save_on_top = True
    save_as = True
    # Для создания дублей информации. Удобно для создания множества объектов
    list_editable = ("draft",)
    fieldsets = (
        # Объединение полей в одну строчку
        (None, {
            "fields": (("title", "tagline"),)
        }),
        # Создание группы полей. Без объединения в одну строчку
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        # Вместо None можно поставить имя группы. Для того чтобы было это в свернутом виде -  "classes": ("collapse",),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )
# Для того чтобы сделать поля в одну строку можно использовать field = (('test1', 'test2', 'test3'),)
# Подходит для того, чтобы убрать из формы какие-то поля. Или указать те поля, которые хотим видеть
# Более правильный вариант группировки полей - fieldsets:
# Указываем кортеж, который будет содержать кортежи, которые будут содержать словарь, где указываем ключ fields и кортеж тех полей, которые используем


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")
    prepopulated_fields = {"url": ("name",)}
    # Делать поле url на основе поля name. Автозаполнение


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie")


admin.site.register(RatingStar)

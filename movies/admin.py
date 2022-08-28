from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .models import *


class MovieAdminForm(forms.ModelForm):
    """
    Форма для подключения к MovieAdmin. В этой форме создаются две
    дополнительных ячейки с переводом. На русском/английском используя
    CKEditorUploadingWidget

    Для подключения формы - в MovieAdmin прописать следующее:
    form = MovieAdminForm
    """
    # description = forms.CharField(
    #     label='Описание',
    #     widget=CKEditorUploadingWidget()
    # )

    description_ru = forms.CharField(
        label='Описание RU', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(
        label='Описание EN', widget=CKEditorUploadingWidget())

    class Meta:
        """Основывается на модели Movie. Перевод будет назначен для
        каждого поля из этой модели"""
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Модель Категорий, наследуется от TranslationAdmin. Благодаря этому
    создаются автоматические поля перевода для доступных языков"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)
    prepopulated_fields = {"url": ("name",)}


#
class ReviewInline(admin.TabularInline):  # admin.StackedInline
    """Модель отзывов на странице фильма. Основывается на TabularInline.

    Служит как инлайн форма для подключения к нужной модели благодаря:
    inlines = [MovieShotsInline, ReviewInline]

    Возможно так же сделать StackedInline, но так будет некрасиво.
    Благодаря TabularInline создание комментариев отображается в строчку, а
    не столбцом

    extra - Дополнительные поля для создания комментариев"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    """Модель кадров из фильма. Наследуется от TabularInline.

    Служит как инлайн форма для подключения к нужной модели благодаря:
    inlines = [MovieShotsInline, ReviewInline]

    Функция get_image с методом mark_safe позволяет отобразить в админке
    фотографии с заданными параметрами. Для работы необходимо сделать
    изображения в readonly_fields кортежем"""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    # Отображение кастомного названия метода
    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Модель фильмов. Наследуется от TranslationAdmin, что позволяет
    автоматически создавать поля для перевода к RU/EN языкам,

    prepopulated_fields - генерирование поля на основе другого поля (slugify)
    {'Генерируемое название': ('На основе этого поля',)}

    inlines - Подключение дополнительных моделей как инлайн формы. Отображение
    тех же кадров из фильма, комментариев основанных на этом фильме. FK/MTM

    """
    # Поля, которые отображаются в админке
    list_display = ("title", "category", "url", "draft")
    # Поля по которым можно фильтровать данные
    list_filter = ("category", "year")
    # Автоматическое генерирование поля url на основе title
    prepopulated_fields = {"url": ("title",)}
    # Поля по которым можно осуществлять поиск в админке
    search_fields = ("title", "category__name")
    # Подключение моделей завязанных на модели фильмов
    inlines = [MovieShotsInline, ReviewInline]
    # Добавить кнопку сохранения сверху
    save_on_top = True
    # Добавить кнопку для сохранения дублей. Для создания множества объектов
    save_as = True
    # Поля которые можно редактировать в админке
    list_editable = ("draft",)
    # Подключение CKEditor
    form = MovieAdminForm
    # Поля только для чтения (Редактировать нельзя)
    readonly_fields = ("get_image",)
    # Регистрация actions (Методов)
    actions = ["publish", "unpublish"]

    # Отображение полей при детальном просмотре группируя их
    fieldsets = (
        # Объединение полей в одну строчку
        (None, {
            "fields": (("title", "tagline"),)
        }),
        ('Информация', {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"),)
        }),
        # Вместо None можно поставить имя группы.
        # Для того чтобы было это в свернутом виде -  "classes": ("collapse",),
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

    # Для того чтобы сделать поля в одну строку можно использовать:
    # field = (('test1', 'test2', 'test3'),)
    # Подходит для того, чтобы убрать из формы какие-то поля.
    # Или указать те поля, которые хотим видеть

    # Более правильный вариант группировки полей - fieldsets:
    # fieldsets = (
    #     ('Название/None', {
    #         "fields": ('поля и их группировка')
    #     }),
    # )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def publish(self, request, queryset):
        """Actions для формы MovieAdmin для добавления указанных фильмов на
        публикацию. На вход получает:
        request - Запрос
        queryset - Выделенные объекты модели"""

        # Количество обновленных строк. Обновляем значение у QuerySet
        # и ставим значение draft=True
        row_update = queryset.update(draft=True)

        # Правильное склонение существительных
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        # Отображение сообщения пользователю
        self.message_user(request, f'{message_bit}')

    # Передает сообщение в административную панель.

    def unpublish(self, request, queryset):
        """Actions для формы MovieAdmin. Метод такой же как и у publish,
        только снимает посты с публикации"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    # Отображение кастомного названия у Actions
    publish.short_description = "Опубликовать"
    # Права, которые пользователь должен иметь для использования Actions
    publish.allowed_permission = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Модель отзывов. Нельзя изменять поля name, email"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Модель жанров. С автоматическим заполнением поля url"""
    list_display = ("name", "url")
    prepopulated_fields = {"url": ("name",)}


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Модель актеров. Отображается картинка с помощью функции get_image"""
    list_display = ("name", "age", 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Модель рейтинга. С фильмом, айпишником и количеством звезд"""
    list_display = ("movie", "ip", "star")


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    """Модель кадров из фильма с отображением картинки"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


# Настройки админки. Изменение title/header
admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

# Регистрация модели RatingStar
admin.site.register(RatingStar)

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    # Поле из Movie, для которого будет применен CKEditor
    # Чтобы подключить - для нужной таблицы - form = MovieAdminForm

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)
    prepopulated_fields = {"url": ("name",)}


#
class ReviewInline(admin.TabularInline):  # admin.StackedInline
    """Отзывы на странице фильма"""
    model = Reviews
    # Модель, которая используется
    extra = 1
    # Дополнительные поля для заполнения
    readonly_fields = ("name", "email")


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    prepopulated_fields = {"url": ("title",)}
    # Делать поле url на основе поля title. Автозаполнение
    search_fields = ("title", "category__name")
    # Поиск по имени категории, через обращение к БД
    inlines = [MovieShotsInline, ReviewInline]
    # inlines - Для MTM FRK. Прикрепление классов к таблице
    save_on_top = True
    save_as = True
    # Для создания дублей информации. Удобно для создания множества объектов
    list_editable = ("draft",)
    form = MovieAdminForm
    # Подключение CKEditor
    readonly_fields = ("get_image",)
    actions = ["publish", "unpublish"]
    # Регистрация actions
    fieldsets = (
        # Объединение полей в одну строчку
        (None, {
            "fields": (("title", "tagline"),)
        }),
        # Создание группы полей. Без объединения в одну строчку "fields": (test1, test2)
        (None, {
            "fields": ("description", ("poster", "get_image"))
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

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    # Передаем запрос и объект модели queryset
    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        # Обновляем поле draft и ставим его в True и проверяем сколько записей было обновлено. Одна или несколько
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    # Передает сообщение в административную панель.

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permission = ('change',)
    # Чтобы применять эту функцию, у пользователя должны быть права на изменения.

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = ('change',)

    get_image.short_description = 'Постер'


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
    list_display = ("name", "age", 'get_image')
    readonly_fields = ('get_image',)

    # Для вывода фотографии в полной записи

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    # Выводить фотографию как хтмл строку

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip", "star")


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = 'Изображение'


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

admin.site.register(RatingStar)

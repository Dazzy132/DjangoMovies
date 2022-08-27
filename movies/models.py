from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie_in_category', kwargs={"slug": self.url})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Модель актеров и режиссеров"""
    name = models.CharField(max_length=150, verbose_name='Имя')
    age = models.PositiveSmallIntegerField(default=0, verbose_name='Возраст')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='actors/', verbose_name='Изображение')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.name})

    class Meta:
        verbose_name = 'Актеры и режиссеры'
        verbose_name_plural = 'Актеры и режиссеры'


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(max_length=150, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильм"""
    title = models.CharField(max_length=150, verbose_name='Название')
    tagline = models.CharField(
        max_length=100, verbose_name='Слоган', default=''
    )
    description = models.TextField(verbose_name='Описание')
    # Фотографии | upload_to - в какую папку загружать
    poster = models.ImageField(upload_to='poster/', verbose_name='Постер')
    # PositiveSmall - нельзя поставить большую дату и меньше 0
    year = models.PositiveSmallIntegerField(
        default='2022', verbose_name='Дата выхода'
    )
    country = models.CharField(max_length=150, verbose_name='Страна')
    # Многие ко многим. У Фильма может быть несколько директоров
    directors = models.ManyToManyField(
        Actor, verbose_name='Режиссеры', related_name='film_director'
    )
    actors = models.ManyToManyField(
        Actor, verbose_name='Актеры', related_name='film_actor'
    )
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    # Мировая премьера. По умолчанию ставится сегодняшний день
    # from datetime import date
    world_premiere = models.DateField(
        default=date.today, verbose_name='Премьера в мире'
    )
    # Бюджет. По умолчанию 0. Бюджет не может быть меньше 0 благодаря
    # PositiveIntegerField, help_text - отображение подсказки в админке
    budget = models.PositiveIntegerField(
        default=0, help_text='Указывать сумму в $', verbose_name='Бюджет'
    )
    fees_in_usa = models.PositiveIntegerField(
        default=0, help_text='Указывать сумму в $', verbose_name='Сборы в США'
    )
    fees_in_world = models.PositiveIntegerField(
        default=0, help_text='Указывать сумму в $', verbose_name='Сборы в мире'
    )
    # При удалении категории, у всех фильмов будет значение Null,
    # и они не удалятся - models.SET_NULL, null=True,
    # фильм может не иметь категорию
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, null=True, verbose_name='Категория'
    )
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField(default=False, verbose_name='Черновик')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        """Дополнительный метод у модели. Получение отзывов.
        Возвращает список отзывов прикрепленных к фильму, фильтруя, где поле
        parent=Null. Это означает, что комментарии закрепленные на комментариях
        отображаться не будут"""
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    """Модель кадров из фильма"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='movie_shots/', verbose_name='Изображение'
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name='Фильм'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    """Модель количества звезд рейтинга"""
    value = models.PositiveSmallIntegerField(
        default=0, verbose_name='Значение'
    )

    def __str__(self):
        # Чтобы добавлять звезды рейтинга, нужно передать её как строку
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        # Отображение звезд в нужном порядке
        ordering = ('value',)


class Rating(models.Model):
    """Модель рейтинга"""
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    star = models.ForeignKey(
        RatingStar, on_delete=models.CASCADE, verbose_name='Звезда'
    )
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name='Фильм'
    )

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField(max_length=100, verbose_name='Имя')
    text = models.TextField(max_length=5000, verbose_name='Сообщение')
    # Запись ссылается на запись в этой же таблице благодаря self
    # Это позволяет отзывы на отзывы
    parent = models.ForeignKey(
        'self',
        verbose_name='Родитель',
        on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

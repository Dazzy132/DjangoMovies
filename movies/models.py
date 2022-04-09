from datetime import date

from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField(max_length=150, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и режиссеры"""
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
    """Жанры"""
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
    tagline = models.CharField(max_length=100, verbose_name='Слоган', default='')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(upload_to='poster/', verbose_name='Постер')
    year = models.PositiveSmallIntegerField(default='2022', verbose_name='Дата выхода')
    country = models.CharField(max_length=150, verbose_name='Страна')
    directors = models.ManyToManyField(Actor, verbose_name='Режиссеры', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField(default=date.today, verbose_name='Премьера в мире')
    budget = models.PositiveIntegerField(default=0, help_text='Указывать сумму в $', verbose_name='Бюджет')
    fees_in_usa = models.PositiveIntegerField(
        default=0, help_text='Указывать сумму в $', verbose_name='Сборы в США'
    )
    fees_in_world = models.PositiveIntegerField(
        default=0, help_text='Указывать сумму в $', verbose_name='Сборы в мире'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория'
    )
    # SET_NULL - Если удаляем категорию, то поле будет равно Null. И указываем что null может быть True
    url = models.SlugField(max_length=150, unique=True)
    draft = models.BooleanField(default=False, verbose_name='Черновик')

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})
    # 'slug' - ключ который запрашиваем в urls.py ( <slug: ) , а self.url - то, что передаем по этому пути

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)
    # Возвращает список отзывов прикрепленных к фильму, фильтруя там где поле parent = Null
    # Оставляет обычные отзывы, комментарии к ним не выводит.

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='movie_shots/', verbose_name='Изображение')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.PositiveSmallIntegerField(default=0, verbose_name='Значение')

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField(max_length=15, verbose_name='IP адрес')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name='Фильм')

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
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    # Запись ссылается на запись в этой же таблице
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    # Кастомное название модели для отображения в админке
    verbose_name = 'Фильмы'

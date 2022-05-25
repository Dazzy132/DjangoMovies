from django import template  # Регистрация темплейт тега.
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


# Передача темплейт тега в шаблон, который нужно будет рендерить
@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    movies = Movie.objects.order_by('-id')[:count]
    return {"last_movies": movies}
# count=5 стоит по умолчанию. Его можно редактировать вызвав функцию {% get_last_movies count=3 %}

# Темлпейттеги создаются для того, чтобы не засирать код. В этом случае, чтобы не засирать views.py для получения списка Категорий, для вывода в header
# Теги подключаются с помощью загрузки тегов {load название_файла} - В текущем случае movie_tag

# Симпл тег полезен для того, чтобы передать информацию.
# Инклюжен тег так же передает информацию, а так же её рендерит.
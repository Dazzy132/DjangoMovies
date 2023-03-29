from django import template

from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    """Передача в шаблон данных для последующего рендеринга
    count=5 по умолчанию. Значение можно изменять вызывая функцию след.
    образом - {% get_last_movies count=3 %}"""
    movies = Movie.objects.order_by('-id')[:count]
    return {"last_movies": movies}

# Подключение тегов - {% load movie_tag %}
# Симпл тег полезен для того, чтобы передать информацию.
# Инклюжн тег так же передает информацию, а так же её рендерит.

from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import *
from .forms import ReviewsForm

class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"
    # template_name можно не указывать если писать шаблоны (Название модели_list) или detail. Зависит от класса
    # context_object_name не указывается, потому что обращение в шаблонах идет непосредственно к имени модели - movie.


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"
    # slug_field - Поле по которому нужно будет искать запись. "url" - поле в модели Movie

class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        # Пост запрос HTTP | request - запрос, pk - id фильма
        form = ReviewsForm(request.POST)
        # Заполнение форму ReviewsForm данными, которые пришли из запроса
        movie = Movie.objects.get(id=pk)
        # Делая запрос в БД на получение записи, найдя фильм по ID получаем объект Movie
        if form.is_valid():
            form = form.save(commit=False)
            # Приостановка сохранения формы для вноса изменений
            form.movie = movie
            # Присваиваем форме объект и сохраняем его
            form.save()
        return redirect(movie.get_absolute_url())
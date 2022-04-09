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

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # С помощью родителя получаем в переменную context - словарь (**kwargs) обязательно
    #     context['categories'] = Category.objects.all()
    #     # Добавляем ключ categories и передаем в него все объекты модели Category
    #     return context
# Вывод списка категорий (такой способ или с помощью темплейт тегов

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
            if request.POST.get('parent', None):
                # В пост запросе ищем ключ parent - имя нашего поля. Если оно будет - выполнит код ниже. None - ничего не выполнит
                form.parent_id = int(request.POST.get('parent'))
                # Так как мы добавляем число, а не объект, то parent_id. Достаем значение, так как оно строковое изначально, обарачиваем в int
            form.movie = movie
            # Присваиваем форме объект и сохраняем его
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'
    # Поле по которому искать актеров - slug_field


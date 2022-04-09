from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import *
from .forms import ReviewsForm


# Похож на метод get_context_data(). Передает свои данные в другие классы
class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()
    # Получение всех жанров

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")
    # Получение всех фильмов которые не черновики, забираем только поле с годом ( values("year") )


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"
    # template_name можно не указывать если писать шаблоны (Название модели_list) или detail. Зависит от класса
    # context_object_name не указывается, потому что обращение в шаблонах идет непосредственно к имени модели - movie.


class MovieDetailView(GenreYear, DetailView):
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


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'
    # Поле по которому искать актеров - slug_field


class FilterMoviesView(GenreYear, ListView):
    """Фильтрация фильмов"""

    def get_queryset(self):
        queryset = Movie.objects.all()
        # Назначаем переменной модель Movie
        if "year" in self.request.GET:
            # Если год есть в запросе
            queryset = queryset.filter(year__in=self.request.GET.getlist("year"))
            # queryset = фильтруем по запрошенному году/годам поле 'year'
        if "genre" in self.request.GET:
            # Если жанр есть в запросе
            queryset = queryset.filter(genres__in=self.request.GET.getlist("genre"))
            # queryset = фильтруем по запрошенному жанр/жанрам поле 'genre'
        return queryset





    # def get_queryset(self):
    #     queryset = Movie.objects.filter(
    #         Q(year__in=self.request.GET.getlist('year')) |
    #         Q(genres__in=self.request.GET.getlist('genre'))
    #     )
    #     # C помощью метода Q можно будет запрашивать или года или жанры. (ИЛИ - | )
    #     return queryset


        # queryset = Movie.objects.filter(
        #     year__in=self.request.GET.getlist('year'), genres__in=self.request.GET.getlist('genre')
        # )
        # Чтобы совпадал и год и жанр



# Фильтруем фильмы, где года будут входить в список, который будет возвращаться с фронтенда.
# Фильтрация равна запросу, с помощью метода GET, достается с помощью getlist(поле которое получаем)
# Чтобы применить фильтрацию, нужно будет обернуть поле в форму и вызвать метод get


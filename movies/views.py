from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .models import *
from .forms import ReviewsForm, RatingForm

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
    paginate_by = 3

class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"

    # slug_field - Поле по которому нужно будет искать запись. "url" - поле в модели Movie

    # Получение формы рейтинга
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewsForm()
        # Для работы Рекаптчи переделана форма. И по этому нужно передавать это поле как form
        return context

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
    paginate_by = 2

    # def get_queryset(self):
    #     queryset = Movie.objects.all()
    #     # Назначаем переменной модель Movie
    #     if "year" in self.request.GET:
    #         # Если год есть в запросе
    #         queryset = queryset.filter(year__in=self.request.GET.getlist("year"))
    #         # queryset = фильтруем по запрошенному году/годам поле 'year'
    #     if "genre" in self.request.GET:
    #         # Если жанр есть в запросе
    #         queryset = queryset.filter(genres__in=self.request.GET.getlist("genre"))
    #         # queryset = фильтруем по запрошенному жанр/жанрам поле 'genre'
    #     return queryset

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = ''.join(f'year={x}&' for x in self.request.GET.getlist('year'))
# Формирование строки из элементов списка, объединяя их с помощью метода join. Запросы приходят с помощью self.get.request.GET.getlist()
# Далее идет построение ссылки с помощью цикла. Проходимся циклом по запросу и достаем оттуда все пришедшие года. Приписываем их к year=2019&.
# & - значит И.
        context['genre'] = ''.join(f'genre={x}&' for x in self.request.GET.getlist('genre'))
        return context

class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        # Когда придет пост запрос - за это отвечает подфункция post
        form = RatingForm(request.POST)
        # В form передаем request.POST
        if form.is_valid():
            # Проверяем на валидность
            Rating.objects.update_or_create(
                # update_or_create - Позволяет обновить или создать запись
                ip=self.get_client_ip(request),
                # ip = Через функцию get_client_ip получаем IP пользователя отправившего запрос
                movie_id=int(request.POST.get("movie")),
                # movie_id = Строковое значение, полученное из запроса. Оборачиваем в int(). Данные приходят со скрытого поля movie
                defaults={'star_id': int(request.POST.get("star"))}
                # В defaults передается словарь{'ключ поля которое нужно изменить': значение, на которое меняем
            )
            # Чтобы не создавались новые записи рейтинга, когда пользователь переставляет её, идет изменение текущей.
            # Пользователь так же не имеет более одной на один фильм
            return HttpResponse(status=201)
        # При успешном вернется статус 201, если нет - 400
        else:
            return HttpResponse(status=400)

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


class Search(ListView):
    """Поиск фильма"""
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))
    # Фильтруем фильмы, по полученному запросу, где название содержит запрос полученный из поля ввода в _sidebar.html с названием q

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        # Добавляем в словарь значение, которое пришло. Это нужно для того, чтобы работала пагинация
        # Чтобы работала пагинация, необходимо передать контенст как строку, где q будет равно запросу.
        # В _pagination.html нужно будет внести её перед другими параметрами {{ q }} {{ year }} {{ genre }}
        return context
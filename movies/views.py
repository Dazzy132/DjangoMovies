from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from .forms import ReviewsForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов. Этот класс для наследования, чтобы
    передать нужные методы для нужных классов. К примеру:
    class MoviesView(GenreYear, ListView):
    """

    def get_genres(self):
        """Получение всех жанров"""
        return Genre.objects.all()

    def get_years(self):
        """Получение всех фильмов, у которых draft=False и забираем значение
        только года этих фильмов"""
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear, ListView):
    """Вывод всех фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movie_list.html"
    # template_name можно не указывать если писать шаблоны
    # (Название модели_list) или detail. Зависит от класса

    # context_object_name не указывается, потому что обращение в шаблонах идет
    # непосредственно к имени модели - movie (movie_list).
    paginate_by = 6


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"
    # slug_field - Поле по которому нужно будет искать запись,
    # "url" - поле в модели Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        context['form'] = ReviewsForm()
        # Для работы Рекаптчи переделана форма.
        # И по этому нужно передавать это поле как form
        return context

    def get_user_stars(self, ip, movie_id):
        """Получить звезды пользователя"""
        if Rating.objects.filter(ip=ip, movie_id=movie_id).exists():
            stars = Rating.objects.get(ip=ip, movie_id=movie_id).star
            # .star - обращение к RatingStar, так как это поле - ForeignKey
        else:
            stars = None
        return stars

    def get(self, request, *args, **kwargs):
        """Отображение количество звезд пользователя по IP"""
        ip = AddStarRating.get_client_ip(self, self.request)
        movie_id = Movie.objects.get(url=kwargs['slug']).id
        stars = self.get_user_stars(ip, movie_id)
        # Получить контекст
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if stars:
            context['stars'] = str(stars)

        return self.render_to_response(context)


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            # Получить имя parent, если нет - то None
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
                # Так как мы добавляем число, а не объект, то parent_id.
                # Достаем значение, так как оно строковое изначально,
                # оборачиваем в int
            form.movie = movie
            # Присваиваем форме объект и сохраняем его
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class FilterMoviesView(GenreYear, ListView):
    """Фильтрация фильмов"""
    paginate_by = 3

    def get_queryset(self):
        """Сделать отборку фильмов по полученным параметрам из request
        Метод GET.getlist заберет данные в виде list
        .distinct() - исключит повторения"""
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    # def get_queryset(self):
    #     """Первый вариант (Плохой) Фильтрации"""
    #     queryset = Movie.objects.all()
    #     if "year" in self.request.GET:
    #         queryset = queryset.filter(
    #             year__in=self.request.GET.getlist("year")
    #         )
    #     if "genre" in self.request.GET:
    #         # Если жанр есть в запросе
    #         queryset = queryset.filter(
    #             genres__in=self.request.GET.getlist("genre")
    #         )
    #     return queryset

    def get_context_data(self, *args, **kwargs):
        """Формирование строки из элементов списка, объединяя их с помощью
        метода join. Запрос с фильтрацией в HTML выглядит так:
        year=2001&year=2002&
        """
        context = super().get_context_data(**kwargs)
        context['year'] = ''.join(
            f'year={x}&' for x in self.request.GET.getlist('year')
        )
        context['genre'] = ''.join(
            f'genre={x}&' for x in self.request.GET.getlist('genre')
        )
        return context


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        """Получить IP пользователя"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                # update_or_create - Позволяет обновить или создать запись
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                # movie_id = Строковое значение, полученное из запроса.
                # Оборачиваем в int(). Данные приходят со скрытого поля movie
                defaults={'star_id': int(request.POST.get("star"))}
                # В defaults передается словарь
                # {'ключ изменяемого поля': значение, на которое меняем
            )
            # Чтобы не создавались новые записи рейтинга,
            # когда пользователь переставляет её, идет изменение текущей.
            # Пользователь так же не имеет более одной оценки на один фильм
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

    # def get_queryset(self):
    #     queryset = Movie.objects.filter(
    #         Q(year__in=self.request.GET.getlist('year')) |
    #         Q(genres__in=self.request.GET.getlist('genre'))
    #     )
    #     # C помощью метода Q можно будет запрашивать
    #     # или года или жанры. (ИЛИ - | )
    #     return queryset
    #
    #     queryset = Movie.objects.filter(
    #         year__in=self.request.GET.getlist('year'),
    #         genres__in=self.request.GET.getlist('genre')
    #     )
    #     Чтобы совпадал и год и жанр


class Search(ListView):
    """Поиск фильма"""
    paginate_by = 2

    def get_queryset(self):
        """Фильтруем фильмы, по полученному запросу, где название содержит
         запрос полученный из поля ввода в _sidebar.html с названием q"""
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        """Добавляем в словарь значение, которое пришло. Это нужно для того,
        чтобы работала пагинация. Чтобы она работала, необходимо передать
        контекст как строку, где q будет равно запросу. В _pagination.html
        нужно будет внести её перед другими параметрами {{ q }} {{ year }}
         {{ genre }}"""
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context


class MovieByCategory(GenreYear, ListView):
    """Отображение фильмов по категориям"""
    template_name = 'movies/categories.html'
    context_object_name = 'movie'
    allow_empty = False

    def get_queryset(self):
        return Movie.objects.filter(category__url=self.kwargs['slug'])
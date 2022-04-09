from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesView.as_view(), name='home'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    # filter стоит выше чтобы данный url не попадал в поле поиска по слагу
    path("<slug:slug>/", MovieDetailView.as_view(), name='movie_detail'),
    # Первый аргумент <slug: - то, что мы запрашиваем в models.py (get_absolute_url). Второй аргумент, то что мы передаем в views.py
    path('review/<int:pk>/', AddReview.as_view(), name="add_review"),
    # Добавление отзывов. Перекидываем на страницу отзыва, pk передаем в views.py
    path('actor/<str:slug>/', ActorView.as_view(), name='actor_detail')
]
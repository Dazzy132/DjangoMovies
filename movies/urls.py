from django.urls import path
from .views import *

urlpatterns = [
    path('', MoviesView.as_view(), name = 'home')
]
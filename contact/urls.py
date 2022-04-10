from django.urls import path
from .views import *

urlpatterns = [
    path('', ContactView.as_view(), name='contact')
    # Создается для связи формы с views.py, чтобы форма создавалась.
]
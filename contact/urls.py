from django.urls import path
from .views import *

# app_name = 'contact'

urlpatterns = [
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('form/', IFrameContactView.as_view(), name='icontact')
]
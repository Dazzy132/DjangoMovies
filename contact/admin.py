from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Отображение модели в админке"""
    list_display = ("email", "date")

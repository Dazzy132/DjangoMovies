from django import forms
from .models import Reviews

class ReviewsForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')
        # Поля которые нужны для отправки формы

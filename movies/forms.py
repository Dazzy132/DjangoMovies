from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, Rating, RatingStar


class ReviewsForm(forms.ModelForm):
    """Форма добавления отзывов с каптчей."""
    # Добавление поля Рекаптчи
    captcha = ReCaptchaField()

    class Meta:
        """По правилам SOLID форму нужно рендерить.
        Для сохранения стилей нужно будет добавлять виджеты
        Для применения классов их нужно будет передавать как список
        через attrs={'class': 'стиль'}"""
        model = Reviews
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }

    # Отображение до добавления Каптчи. Просто как HTML форму
    # class Meta:
    #     model = Reviews
    #     fields = ('name', 'email', 'text')


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга. Используется ModelChoiceField, чтобы
    добавить выбор звезд на основе модели RatingStar,
    widget - Как форма будет выглядеть в HTML представлении
    (Выпадающий список / Checkbox / Radio-box)
    empty_label - Что будет отображаться при виде формы выбора изначально"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ('star',)
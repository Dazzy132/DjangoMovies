from django import forms
from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Reviews, Rating, RatingStar


class ReviewsForm(forms.ModelForm):
    """Форма отзывов"""
    captcha = ReCaptchaField()
    # Добавление поля Рекаптчи

    class Meta:
        model = Reviews
        fields = ("name", "email", "text", "captcha")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border"}),
            "email": forms.EmailInput(attrs={"class": "form-control border"}),
            "text": forms.Textarea(attrs={"class": "form-control border"})
        }
    # По правилам SOLID форму нужно рендерить. Для сохранения стилей нужно будет добавлять виджеты.
    # Для применения классов их нужно будет передавать как список через attrs={'class': 'стиль'}

    # class Meta:
    #     model = Reviews
    #     fields = ('name', 'email', 'text')
    #     # Поля которые нужны для отправки формы
# Просто html


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )
    # Чтобы выводить список звезд, нужно переопределить поле star.
    # Создаем форму выбора. Queryset = все звезды которые мы создали | widget - то, как будет представлена форма в HTML. Меняя виджеты, меняем вид форму.
    # Выпадающий список / Checkbox / Radio-box
    # Данную форму нужно отобразить на странице описания фильма. Для этого импортируем форму во Views

    class Meta:
        model = Rating
        fields = ('star',)
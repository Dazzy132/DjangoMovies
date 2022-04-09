from django import forms
from .models import Reviews, Rating, RatingStar


class ReviewsForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ('name', 'email', 'text')
        # Поля которые нужны для отправки формы


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
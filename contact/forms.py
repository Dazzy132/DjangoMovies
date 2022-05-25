from django import forms    # Для работы с формами
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField     # Импорт каптчи


# Сделать форму, которая наследуется от уже созданной модели
class ContactForm(forms.ModelForm):
    """Форма отправки по Email"""
    captcha = ReCaptchaField()   # Подключение Каптчи

    class Meta:
        model = Contact
        fields = ("email",)     # Поля для заполнения
        widgets = {
            "email": forms.TextInput(attrs={"class": "editContent", 'placeholder': "Your Email..."})
            # editContent - тот же класс, который использовался в форме
            # placeholder - Что отображать в текстовом поле
        }
        labels = {
            "email": ''
        }
        # Как я понял labels для корректного отображения. В этом случае сработало как перенос на след строчку

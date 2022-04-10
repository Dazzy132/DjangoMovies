from django import forms
from .models import Contact
from snowpenguin.django.recaptcha3.fields import ReCaptchaField


# Импорт форм, для работы. Контактов, Каптчи

class ContactForm(forms.ModelForm):
    """Форма отправки по Email"""
    captcha = ReCaptchaField()

    # Подключение Каптчи

    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(attrs={"class": "editContent", 'placeholder': "Your Email..."})
            # editContent - тот же класс, который использовался в форме
        }
        labels = {
            "email": ''
        }
        # Как я понял labels для корректного отображения. В этом случае сработало как перенос на след строчку

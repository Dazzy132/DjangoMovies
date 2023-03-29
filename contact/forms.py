from django import forms  # Для работы с формами
# from snowpenguin.django.recaptcha3.fields import ReCaptchaField

from .models import Contact


class ContactForm(forms.ModelForm):
    """Форма отправки по Email"""
    # captcha = ReCaptchaField()

    class Meta:
        model = Contact
        fields = ("email",)
        widgets = {
            "email": forms.TextInput(
                attrs={"class": "editContent",
                       'placeholder': "Введите почту..."})
        }
        labels = {'email': ''}

    def clean_email(self):
        email = self.cleaned_data['email']
        if Contact.objects.filter(email=email).exists():
            raise forms.ValidationError('Такой email уже подписан на нас')
        return email

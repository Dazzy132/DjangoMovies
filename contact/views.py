from django.urls import reverse
from django.views.generic import CreateView, TemplateView

from .forms import ContactForm


class ThanksView(TemplateView):
    """Отображение страницы Спасибо"""
    template_name = 'contact/thanks.html'


class IFrameContactView(CreateView):
    """Форма подписки по email"""
    form_class = ContactForm
    template_name = 'contact/contact_form.html'

    def get_success_url(self):
        return reverse('thanks')

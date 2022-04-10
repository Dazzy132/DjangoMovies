from django.views.generic import CreateView

from .models import Contact
from .forms import ContactForm


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    success_url = "/"
# При удачном срабатывании перекидывать на главную


# Создаем класс для обработки формы. Передаем туда модель контактов и форму.
# CreateView - для работы с формами.


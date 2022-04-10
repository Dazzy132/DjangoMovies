from django import template
from contact.forms import ContactForm

register = template.Library()


@register.inclusion_tag("contact/tags/form.html")
def contact_form():
    return {"contact_form": ContactForm()}

# Этот файл используется для того, чтобы создать поле ввода формы email. Для этого её вырезали с футера, создали в templates новую папку contact/tags/form.html
# Создаем функцию contact_form, в которую передаем форму и передаем её в html файл.

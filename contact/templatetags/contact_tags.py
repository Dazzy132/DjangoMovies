from django import template
from contact.forms import ContactForm

register = template.Library()


@register.inclusion_tag("contact/tags/form.html")
def contact_form():
    """Передача контакт формы в файл form.html"""
    return {"contact_form_tag": ContactForm()}

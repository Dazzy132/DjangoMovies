from django import template

register = template.Library()

@register.filter(name='attr')
def set_attribute(value, arg):
    """Установить аттрибут к любому полю формы
    Пример: {{ form.name|attr:"id:contactcomment" }}
    """
    attrs = {}
    definition = arg.split(':')
    if len(definition) == 2:
        attrs[definition[0]] = definition[1]
    else:
        attrs[definition[0]] = True
    return value.as_widget(attrs=attrs)
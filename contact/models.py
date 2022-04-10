from django.db import models

# Create your models here.
class Contact(models.Model):
    """Подписка по Email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    # Автоматически создает время

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
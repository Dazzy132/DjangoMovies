from django.db import models


class Contact(models.Model):
    """Подписка по Email"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)
    # Автоматически создает время (auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
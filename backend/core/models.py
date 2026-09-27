from django.db import models
from django.utils.translation import gettext_lazy as _

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Создано"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Обновлено"))

    class Meta:
        abstract = True


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Название города"))

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']

    def __str__(self):
        return self.name

from django.db import models
from django.urls import reverse


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Город')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Городов'
        ordering = ['name']

    def get_absolute_url(self): # generate link for unique obj.
        return reverse('cities:detail', kwargs={'pk': self.pk})
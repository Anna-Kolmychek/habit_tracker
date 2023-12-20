from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='создатель', **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место выполнения', **NULLABLE)
    time_when = models.TimeField(verbose_name='время, когда выполнять', **NULLABLE)
    action = models.CharField(max_length=150, verbose_name='действие')
    is_pleasant = models.BooleanField(verbose_name='признак приятной привычки', default=False)
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='связанная привычка', **NULLABLE)
    periodical = models.PositiveIntegerField(default=1, verbose_name='периодичность (в днях)')
    reward = models.CharField(max_length=150, verbose_name='вознаграждение', **NULLABLE)
    time_duration = models.PositiveIntegerField(verbose_name='время выполнения (в сек.)', **NULLABLE)
    is_public = models.BooleanField(verbose_name='признак приятной привычки', default=False)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

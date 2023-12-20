from django.db import models

from habits.models import Habit


class TgUser(models.Model):
    tg_chat_id = models.CharField(max_length=50, verbose_name='chatID пользователя')

    def __str__(self):
        return f'{self.pk} - {self.tg_chat_id}'

    class Meta:
        verbose_name = 'Пользователь в ТГ'
        verbose_name_plural = 'Пользователи в ТГ'


class TgMessage(models.Model):
    tg_chat_id = models.ForeignKey(TgUser, verbose_name='chatID пользователя', on_delete=models.CASCADE)
    habit = models.ForeignKey(Habit, verbose_name='привычка', on_delete=models.CASCADE)
    msg_date = models.DateField(verbose_name='дата отправки сообщения')

    def __str__(self):
        return f'({self.msg_date}) {self.tg_chat_id} - {self.habit}'

    class Meta:
        verbose_name = 'Сообщение в ТГ'
        verbose_name_plural = 'Сообщения в ТГ'

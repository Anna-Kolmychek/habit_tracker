from datetime import date

import requests
from django.conf import settings

from habits.models import Habit
from tg_bot.models import TgUser, TgMessage

TG_BOT_TOKEN = settings.TG_BOT_TOKEN
TG_URL = settings.TG_URL


def get_new_tg_users(updates):
    """Обработка новых сообщений: получение новых пользователей и id последнего обновления"""
    update_id = None
    for update in updates:
        update_id = update.get('update_id')
        chat_id = str(update.get('message').get('from').get('id'))
        msg = update.get('message').get('text')

        tg_user = TgUser.objects.filter(tg_chat_id=chat_id).first()

        if msg == '/start':
            if not tg_user:
                tg_user = TgUser.objects.create(tg_chat_id=chat_id)
            start_msg = 'Привет! Я буду высылать тебе напоминания о привычках'
            send_tg_msg(tg_user, start_msg)

    return update_id


def send_tg_msg(tg_user, msg):
    """отправка в ТГ сообщения"""

    chat_id = int(tg_user.tg_chat_id)
    data = {'chat_id': chat_id, 'text': msg}

    try:
        requests.post(f'{TG_URL}{TG_BOT_TOKEN}/sendMessage', data=data)
    except Exception:
        print('Send msg error')


def filter_habits():
    return Habit.objects.filter(
        is_public=True,
        is_pleasant__in=[False, None]
    )


def send_reminder(habits):
    print(habits)
    for tg_user in TgUser.objects.all():
        tg_messages = tg_user.tgmessage_set.all()
        for habit in habits:
            msg = (f'Выполните действие: {habit.action}\n'
                   f'Где: {habit.place}, когда: {habit.time_when}\n'
                   f'Вознаграждение - {habit.reward if habit.reward else habit.related_habit.action}\n')
            tg_message = tg_messages.filter(habit=habit).first()
            if not tg_message:
                send_tg_msg(tg_user, msg)
                TgMessage.objects.create(
                    tg_chat_id=tg_user,
                    habit=habit,
                    msg_date=date.today()
                )
            elif (tg_message.msg_date - date.today()).days >= tg_message.habit.periodical:
                tg_message.msg_date = date.today()
                send_tg_msg(tg_user, msg)

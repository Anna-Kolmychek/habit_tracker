import requests
from celery import shared_task
from django.conf import settings

from tg_bot.services import get_new_tg_users, filter_habits, send_reminder

TG_BOT_TOKEN = settings.TG_BOT_TOKEN
TG_URL = settings.TG_URL


@shared_task
def get_tg_bot_update():
    update_id = settings.TG_BOT_UPDATE_OFFSET
    data = {'offset': update_id}
    request = requests.post(f'{TG_URL}{TG_BOT_TOKEN}/getUpdates', data=data)
    if request.status_code == 200:
        if request.json()['ok']:
            update_id = get_new_tg_users(request.json()['result'])
            if update_id:
                settings.TG_BOT_UPDATE_OFFSET = update_id + 1


@shared_task
def check_habits():
    habits = filter_habits()
    send_reminder(habits)

# Generated by Django 5.0 on 2023-12-19 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_chat_id', models.IntegerField(verbose_name='chatID пользователя')),
            ],
            options={
                'verbose_name': 'Пользователь в ТГ',
                'verbose_name_plural': 'Пользователи в ТГ',
            },
        ),
    ]

# Generated by Django 5.0 on 2023-12-19 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='time_when',
            field=models.TimeField(blank=True, null=True, verbose_name='время, когда выполнять'),
        ),
    ]

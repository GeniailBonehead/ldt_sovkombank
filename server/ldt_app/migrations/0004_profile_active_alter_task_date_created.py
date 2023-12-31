# Generated by Django 4.2.7 on 2023-11-08 21:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ldt_app', '0003_profile_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active',
            field=models.CharField(choices=[('Active', 'На рабочем месте'), ('Vacation', 'В отпуске'), ('Ill', 'На больничном'), ('Duty', 'В командировке'), ('Other', 'Занимается другими задачами')], default='Active', max_length=30, verbose_name='Статус сотрудника'),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 8, 21, 52, 50, 333203), verbose_name='Дата и время создания'),
        ),
    ]

from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (
    Group, Permission, PermissionsMixin, User, UserManager,
)
from django.core.validators import EmailValidator
from django.db import models


class Profile(models.Model):
    """Данные пользователя"""
    USER_GRADE_CHOICES = (
        ('Junior', 'Младший'),
        ('Middle', 'Средний'),
        ('Senjor', 'Старший'),
    )
    USER_STATUS_CHOICES = (
        ('Active', 'На рабочем месте'),
        ('Vacation', 'В отпуске'),
        ('Ill', 'На больничном'),
        ('Duty', 'В командировке'),
        ('Other', 'Занимается другими задачами'),
    )

    user = models.OneToOneField(
        User,
        verbose_name='Учётные данные пользователя',
        on_delete=models.CASCADE,
        default=-1,
    )
    grade = models.CharField(
        verbose_name='Уровень',
        max_length=30,
        choices=USER_GRADE_CHOICES,
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20,
    )
    lastname = models.CharField(
        verbose_name='Фамилия',
        max_length=50,
        blank=False,
    )
    name = models.CharField(
        verbose_name='Имя',
        max_length=50,
        blank=False,
    )
    patronymic = models.CharField(
        verbose_name='Отчество',
        max_length=50,
        blank=False,
    )
    network = models.JSONField(
        verbose_name='Соцсети',
        blank=True,
    )
    active = models.CharField(
        verbose_name='Статус сотрудника',
        max_length=30,
        choices=USER_STATUS_CHOICES,
        default='Active',
    )
    token = models.CharField(
        verbose_name='Токен',
        max_length=50,
        unique=True,
        default='',
    )


class Task(models.Model):
    TASK_TYPE_CHOICES = (
        ('TRAVEL', 'Выезд на точку'),
        ('TEACH', 'Обучение агента'),
        ('CARD', 'Доставка карт'),
    )
    TASK_STATUS_CHOICES = (
        ('FREE', 'Свободна'),
        ('TAKEN', 'В работе'),
        ('ALARM', 'Форс-мажор'),
        ('FINISHED', 'Завершена'),
    )
    TASK_PRIORITY_CHOICES = (
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
    )

    user = models.ForeignKey(
        User,
        verbose_name='Назначенный сотрудник',
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
        db_index=True,
    )
    date_created = models.DateTimeField(
        verbose_name='Дата и время создания',
        default=datetime.now(),
    )
    date_finished = models.DateTimeField(
        verbose_name='Дата и время выполнения',
        null=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=50,
        default='Задача',
    )
    description = models.TextField(
        verbose_name='Описание задачи',
        default='',
    )
    task_type = models.CharField(
        verbose_name='Тип задачи',
        max_length=30,
        choices=TASK_TYPE_CHOICES,
    )
    status = models.CharField(
        verbose_name='Статус',
        max_length=30,
        choices=TASK_STATUS_CHOICES,
    )
    priority = models.IntegerField(
        verbose_name='Приоритет',
        choices=TASK_PRIORITY_CHOICES,
    )


class TaskHistory(models.Model):
    class Meta:
        verbose_name = 'История изменений задачи'
        verbose_name_plural = 'История изменений задачи'

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        help_text='Задача'
    )

    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        help_text='Пользователь производивший изменение статуса задачи',
    )

    old_status = models.CharField(
        verbose_name='Старый статус',
        max_length=32,
        blank=True,
        null=True,
        choices=Task.TASK_STATUS_CHOICES,
        help_text='Предыдущий статус задачи'
    )

    new_status = models.CharField(
        verbose_name='Новый статус',
        max_length=32,
        choices=Task.TASK_STATUS_CHOICES,
        help_text='Новый статус задачи'
    )

    change_datetime = models.DateTimeField(
        verbose_name='Дата и время изменения статуса',
        auto_now_add=True,
        help_text='Дата и время изменения статуса',
    )


class Gis(models.Model):
    """Координаты пользователей"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    lat = models.FloatField(
        verbose_name='Широта',
    )
    long = models.FloatField(
        verbose_name='Долгота',
    )

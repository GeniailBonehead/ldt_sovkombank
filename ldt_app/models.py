from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group, Permission


class CustomUser(AbstractUser):
    """Пользователь"""
    USER_GRADE_CHOICES = (
        ('Junior', 'Младший'),
        ('Middle', 'Средний'),
        ('Senjor', 'Старший'),
    )

    grade = models.CharField(
        verbose_name='Уровень',
        max_length=30,
        choices=USER_GRADE_CHOICES,
    )
    groups = Group
    user_permissions = Permission


class Task(models.Model):
    TASK_TYPE_CHOICES = (
        ('TRAVEL', 'Выезд на точку'),
        ('TEACH', 'Обучение агента'),
        ('CARD', 'Доставка карт'),
    )
    TASK_STATUS_CHOICES = (
        ('FREE', 'Свободна'),
        ('TAKEN', 'В работе'),
        ('FINISHED', 'Завершена'),
    )
    TASK_PRIORITY_CHOICES = (
        (1, 'Низкий'),
        (2, 'Средний'),
        (3, 'Высокий'),
    )

    start_dt = models.DateTimeField(
        verbose_name='Дата и время создания',
        default=datetime.now(),
    )
    end_dt = models.DateTimeField(
        verbose_name='Дата и время выполнения',
        null=True,
    )
    type = models.CharField(
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
    assigned_user = models.ForeignKey(
        CustomUser,
        verbose_name='Назначенный сотрудник',
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
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
        CustomUser,
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

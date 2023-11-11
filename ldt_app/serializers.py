from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from ldt_app.models import (
    Profile,
    Task,
    TaskHistory,
)


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=False)
    date_created = serializers.DateTimeField(required=True)
    date_finished = serializers.DateTimeField(required=False)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    task_type = serializers.ChoiceField(choices=Task.TASK_TYPE_CHOICES, required=True)
    status = serializers.ChoiceField(choices=Task.TASK_STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=Task.TASK_PRIORITY_CHOICES)

    def create(self, validated_data):
        """Создание новой задачи"""
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление задачи"""
        instance.date_created = validated_data.get('start_dt', instance.date_created)
        instance.date_finished = validated_data.get('end_dt', instance.date_finished)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.task_type = validated_data.get('type', instance.task_type)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('start_dt', instance.priority)
        task = Task.objects.get(validated_data.get('id'))
        request = self.context.get("request")
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        if not user:
            return
        if task.status != instance.status:
            TaskHistory.objects.create(task, user, task.status, instance.status, datetime.now)
        instance.save()
        return instance


class ProfileSerializer(serializers.Serializer):
    """Сериалайзер для информации о пользователе"""
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    grade = serializers.ChoiceField(choices=Profile.USER_GRADE_CHOICES)
    email = serializers.CharField(read_only=False)
    phone = serializers.CharField(read_only=True)
    username = serializers.CharField(read_only=True)
    patronymic = serializers.CharField(read_only=True)
    lastname = serializers.CharField(read_only=True)
    network = serializers.JSONField()

    def create(self, validated_data):
        """Создание нового профиля"""
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление профиля"""
        instance.user = validated_data.get('user_id', instance.user)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.username = validated_data.get('username', instance.username)
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.network = validated_data.get('network', instance.network)


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "username", "password")


class TaskHistorySerializer(serializers.Serializer):
    """Сериалайзер истории задач"""

    task = serializers.IntegerField()
    user = serializers.IntegerField()
    old_status = serializers.CharField()
    new_status = serializers.CharField()
    change_datetime = serializers.DateTimeField()


class GisSerializer(serializers.Serializer):
    """Сериалайзер координат"""

    user = serializers.IntegerField()
    lat = serializers.FloatField()
    long = serializers.FloatField()

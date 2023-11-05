from rest_framework import serializers
from ldt_app.models import Task


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    start_dt = serializers.DateTimeField(required=True)
    end_dt = serializers.DateTimeField(required=False)
    type = serializers.ChoiceField(choices=Task.TASK_TYPE_CHOICES, required=True)
    status = serializers.ChoiceField(choices=Task.TASK_STATUS_CHOICES)
    priority = serializers.ChoiceField(choices=Task.TASK_PRIORITY_CHOICES)

    def create(self, validated_data):
        """Создание новой задачи"""
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновление задачи"""
        instance.start_dt = validated_data.get('start_dt', instance.start_dt)
        instance.end_dt = validated_data.get('end_dt', instance.end_dt)
        instance.type = validated_data.get('type', instance.type)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('start_dt', instance.priority)
        instance.save()
        return instance

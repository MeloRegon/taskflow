from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(serializers.Serializer):
    # project_id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)


class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100, required=False) # Необязательные поля
    status = serializers.IntegerField(required=False)


from rest_framework import serializers
from django.utils import timezone
from .models import Task, SubTask, Category


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


#  Переопределение полей сериализатора
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = SubTask
        fields = '__all__'


#  Переопределение методов create и update
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    
    def create(self, validated_data):
        category_name = validated_data.get('name')
        if Category.objects.filter(name=category_name).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        category_name = validated_data.get('name', instance.name)
        if Category.objects.filter(name=category_name).exclude(id=instance.id).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        instance.name = category_name
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


# Базовый сериализатор для SubTask
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'


#  Использование вложенных сериализаторов
class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at', 'subtasks']
        read_only_fields = ['id', 'created_at', 'updated_at']


#  Валидация данных в сериализаторах
class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
    
    def validate_deadline(self, value):
        if value and value < timezone.now():
            raise serializers.ValidationError("Deadline cannot be in the past.")
        return value

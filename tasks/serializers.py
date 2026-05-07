from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Task, SubTask, Category


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже существует.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже существует.')
        return value

    def validate_password(self, value):
        if not any(c.isdigit() for c in value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну цифру.')
        if not any(c.isalpha() for c in value):
            raise serializers.ValidationError('Пароль должен содержать хотя бы одну букву.')
        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Пароли не совпадают.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 'created_at', 'updated_at', 'owner']
        read_only_fields = ['id', 'created_at', 'updated_at', 'owner']


#  Переопределение полей сериализатора
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['owner']


#  Переопределение методов create и update
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['is_deleted', 'deleted_at', 'created_at']


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

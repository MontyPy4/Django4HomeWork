from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name

class Task(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    categories = models.ManyToManyField(Category, verbose_name="Категории задачи", related_name='tasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус задачи")
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ['-created_at']
        unique_together = ['title', 'created_at']  # Уникальность title для даты

    def __str__(self):
        return self.title

class SubTask(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In progress'),
        ('pending', 'Pending'),
        ('blocked', 'Blocked'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название подзадачи")
    description = models.TextField(verbose_name="Описание подзадачи")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Основная задача", related_name='subtasks')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус задачи")
    deadline = models.DateTimeField(verbose_name="Дедлайн")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания")

    class Meta:
        verbose_name = "Подзадача"
        verbose_name_plural = "Подзадачи"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

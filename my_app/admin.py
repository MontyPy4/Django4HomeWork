from django.contrib import admin
from .models import Category, Task, SubTask

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'categories', 'deadline', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'categories')
        }),
        ('Статус и сроки', {
            'fields': ('status', 'deadline')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'task', 'deadline', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'task')
        }),
        ('Статус и сроки', {
            'fields': ('status', 'deadline')
        }),
        ('Системная информация', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']

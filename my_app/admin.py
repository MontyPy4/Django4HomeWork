from django.contrib import admin
from .models import Category, Task, SubTask


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ['title', 'description', 'status', 'deadline']
    show_change_link = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['short_title', 'status', 'deadline', 'created_at']
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
    inlines = [SubTaskInline]

    def short_title(self, obj):
        return obj.title[:10] + '...' if len(obj.title) > 10 else obj.title
    short_title.short_description = 'Название'

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'task', 'status', 'deadline', 'created_at']
    list_filter = ['status', 'task', 'deadline', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['status']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    actions = ['mark_as_done']

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
    @admin.action(description='Отметить выбранные подзадачи как Done')
    def mark_as_done(self, request, queryset):
        updated = queryset.update(status='done')
        self.message_user(request, f'{updated} подзадач отмечено как Done.')

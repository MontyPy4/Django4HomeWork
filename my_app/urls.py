from django.urls import path
from .views import home, create_tasks, read_tasks_subtasks, update_tasks_subtasks, delete_tasks_subtasks

urlpatterns = [
    path('', home, name='home'),                # Главная страница
    path('create/', create_tasks),              # Создание записей (Task и SubTask)
    path('read/', read_tasks_subtasks),         # Чтение записей
    path('update/', update_tasks_subtasks),     # Обновление записей
    path('delete/', delete_tasks_subtasks),     # Удаление записей
]

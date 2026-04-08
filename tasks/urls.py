from django.urls import path
from . import views

urlpatterns = [
    # Сохраняем существующие функции для статистики и специальных эндпоинтов
    path('statistics/', views.task_statistics, name='task_statistics'),
    path('by-weekday/', views.tasks_by_weekday, name='tasks_by_weekday'),
    path('subtasks/filtered/', views.subtasks_filtered, name='subtasks_filtered'),
    
    # Задание 1: Generic Views для задач
    path('tasks/', views.TaskListCreateView.as_view(), name='task_list_create'),
    path('tasks/<int:id>/', views.TaskDetailUpdateDeleteView.as_view(), name='task_detail_update_delete'),
    
    # Задание 2: Generic Views для подзадач
    path('subtasks/', views.SubTaskListCreateView.as_view(), name='subtask_list_create'),
    path('subtasks/<int:pk>/', views.SubTaskDetailUpdateDeleteView.as_view(), name='subtask_detail_update_delete'),
    
    # Обратная совместимость со старыми эндпоинтами
    path('list/', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
]

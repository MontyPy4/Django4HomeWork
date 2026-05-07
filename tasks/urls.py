from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')
router.register('tasks', views.TaskViewSet, basename='task')
router.register('subtasks', views.SubTaskViewSet, basename='subtask')

urlpatterns = [
    path('', include(router.urls)),
    path('statistics/', views.task_statistics, name='task_statistics'),
    path('by-weekday/', views.tasks_by_weekday, name='tasks_by_weekday'),
    path('subtasks/filtered/', views.subtasks_filtered, name='subtasks_filtered'),
    path('list/', views.task_list, name='task_list'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
]

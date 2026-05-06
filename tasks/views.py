from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime
from .models import Task, SubTask, Category
from .serializers import TaskSerializer, SubTaskCreateSerializer, SubTaskSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

    @action(detail=True, methods=['get'])
    def count_tasks(self, request, pk=None):
        category = self.get_object()
        return Response({
            'category_id': category.id,
            'task_count': category.tasks.count(),
        })


@api_view(['POST'])
def create_task(request: Request) -> Response:
    try:
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_list(request: Request) -> Response:
    try:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_detail(request: Request, task_id: int) -> Response:
    try:
        task = Task.objects.get(id=task_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response(data={'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def task_statistics(request: Request) -> Response:
    try:
        total_tasks = Task.objects.count()
        
        pending_tasks = Task.objects.filter(status='pending').count()
        in_progress_tasks = Task.objects.filter(status='in_progress').count()
        completed_tasks = Task.objects.filter(status='completed').count()
        
        current_time = timezone.now()
        overdue_tasks = Task.objects.filter(
            deadline__lt=current_time,
            status__in=['pending', 'in_progress']
        ).count()
        
        statistics = {
            'total_tasks': total_tasks,
            'tasks_by_status': {
                'pending': pending_tasks,
                'in_progress': in_progress_tasks,
                'completed': completed_tasks,
            },
            'overdue_tasks': overdue_tasks,
        }
        
        return Response(statistics, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


#  Эндпоинт для фильтрации задач по дню недели
@api_view(['GET'])
def tasks_by_weekday(request: Request) -> Response:
    try:
        weekday_param = request.query_params.get('weekday', None)
        
        if weekday_param:
            # Словарь соответствия русских названий дней недели с числами
            weekday_mapping = {
                'понедельник': 0,
                'вторник': 1,
                'среда': 2,
                'четверг': 3,
                'пятница': 4,
                'суббота': 5,
                'воскресенье': 6,
                'monday': 0,
                'tuesday': 1,
                'wednesday': 2,
                'thursday': 3,
                'friday': 4,
                'saturday': 5,
                'sunday': 6
            }
            
            weekday_lower = weekday_param.lower()
            if weekday_lower not in weekday_mapping:
                return Response(
                    data={'error': 'Invalid weekday. Use: понедельник, вторник, среда, четверг, пятница, суббота, воскресенье'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            target_weekday = weekday_mapping[weekday_lower]
            tasks = Task.objects.filter(
                deadline__week_day=target_weekday + 1  # Django использует 1-7 (воскресенье=1)
            )
        else:
            # Если параметр не передан, возвращаем все задачи
            tasks = Task.objects.all()
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


# Задание 1: Generic Views для задач
class TaskListCreateView(ListCreateAPIView):
    """
    Generic View для создания и получения списка задач
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['gte', 'lte', 'exact']
    }
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline', 'title']
    ordering = ['-created_at']


class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Generic View для получения, обновления и удаления задач
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


#  Класс пагинации для подзадач
class SubTaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


#  Эндпоинт для фильтрации подзадач по названию задачи и статусу
@api_view(['GET'])
def subtasks_filtered(request: Request) -> Response:
    try:
        task_title = request.query_params.get('task_title', None)
        subtask_status = request.query_params.get('status', None)
        
        # Базовый запрос с сортировкой по убыванию даты
        subtasks = SubTask.objects.all().order_by('-created_at')
        
        # Фильтрация по названию главной задачи
        if task_title:
            subtasks = subtasks.filter(task__title__icontains=task_title)
        
        # Фильтрация по статусу подзадачи (completed/incomplete)
        if subtask_status is not None:
            if subtask_status.lower() in ['true', '1', 'completed', 'завершено']:
                subtasks = subtasks.filter(completed=True)
            elif subtask_status.lower() in ['false', '0', 'incomplete', 'незавершено']:
                subtasks = subtasks.filter(completed=False)
            else:
                return Response(
                    data={'error': 'Invalid status parameter. Use: true/false, completed/incomplete, 1/0'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Применение пагинации
        paginator = SubTaskPagination()
        paginated_subtasks = paginator.paginate_queryset(subtasks, request)
        
        serializer = SubTaskSerializer(paginated_subtasks, many=True)
        return paginator.get_paginated_response(serializer.data)
        
    except Exception as e:
        return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


# Задание 2: Generic Views для подзадач
class SubTaskListCreateView(ListCreateAPIView):
    """
    Generic View для создания и получения списка подзадач
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'completed': ['exact'],
        'task__deadline': ['gte', 'lte', 'exact']
    }
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title', 'task__title']
    ordering = ['-created_at']


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Generic View для получения, обновления и удаления подзадач
    """
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    lookup_field = 'pk'

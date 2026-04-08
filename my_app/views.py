from django.http import HttpResponse
from datetime import date, timedelta
from .models import Task, SubTask

# Главная страница
def home(request):
    return HttpResponse("Hello, Daryna")

# Задание 1: Создание записей
def create_tasks(request):
    # Создаём Task
    task = Task.objects.create(
        title="Prepare presentation",
        description="Prepare materials and slides for the presentation",
        status="New",
        deadline=date.today() + timedelta(days=3)
    )

    # Создаём SubTasks
    SubTask.objects.create(
        task=task,
        title="Gather information",
        description="Find necessary information for the presentation",
        status="New",
        deadline=date.today() + timedelta(days=2)
    )

    SubTask.objects.create(
        task=task,
        title="Create slides",
        description="Create presentation slides",
        status="New",
        deadline=date.today() + timedelta(days=1)
    )

    return HttpResponse("Tasks and SubTasks successfully created!")

# Задание 2: Чтение записей
def read_tasks_subtasks(request):
    new_tasks = Task.objects.filter(status="New")
    overdue_subtasks = SubTask.objects.filter(status="Done", deadline__lt=date.today())

    response_html = "<h2>Tasks со статусом 'New'</h2><ul>"
    for task in new_tasks:
        response_html += f"<li>{task.title} — {task.deadline}</li>"
    response_html += "</ul>"

    response_html += "<h2>SubTasks со статусом 'Done' и просроченные'</h2><ul>"
    for subtask in overdue_subtasks:
        response_html += f"<li>{subtask.title} — {subtask.deadline}</li>"
    response_html += "</ul>"

    return HttpResponse(response_html)

# Задание 3: Изменение записей
def update_tasks_subtasks(request):
    try:
        task = Task.objects.get(title="Prepare presentation")
        task.status = "In progress"
        task.save()
    except Task.DoesNotExist:
        pass

    try:
        subtask1 = SubTask.objects.get(title="Gather information")
        subtask1.deadline = date.today() - timedelta(days=2)
        subtask1.save()
    except SubTask.DoesNotExist:
        pass

    try:
        subtask2 = SubTask.objects.get(title="Create slides")
        subtask2.description = "Create and format presentation slides"
        subtask2.save()
    except SubTask.DoesNotExist:
        pass

    return HttpResponse("Tasks and SubTasks successfully updated!")


from django.http import HttpResponse
from .models import Task, SubTask

def delete_tasks_subtasks(request):
    # все задачи с title "Prepare presentation" и удаляем их вместе с подзадачами
    tasks = Task.objects.filter(title="Prepare presentation")

    # Удаляние подзадачи всех найденных задач
    SubTask.objects.filter(task__in=tasks).delete()

    tasks.delete()

    return HttpResponse("Task 'Prepare presentation' и все её SubTasks удалены (если они были).")
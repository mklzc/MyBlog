from datetime import timedelta

from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from task_manager.tasks import schedule_task, remove_task
import json

def task_list(request):
    status_order = Case(
        When(status='pending', then=Value(1)),  # 未完成 (最前)
        When(status='overdue', then=Value(2)),  # 已逾期 (其次)
        When(status='completed', then=Value(3)),  # 已完成 (最后)
        output_field=IntegerField(),
    )

    tasks = Task.objects.all().order_by(status_order, 'deadline')

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        task_data = [
            {
                "id": task.id,
                "name": task.name,
                "source": task.source,
                "description": task.description,
                "deadline": task.deadline.strftime("%Y-%m-%d %H:%M:%S"),
                "status": task.get_status_display(),
            }
            for task in tasks
        ]
        return JsonResponse({"tasks": task_data})

    return render(request, "task_list.html", {"tasks": tasks})

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            previous_day = task.deadline - timedelta(days=1)
            schedule_task(task.pk, previous_day.strftime("%Y-%m-%d %H:%M:%S"))
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "task_form.html", {"form": form})

def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            previous_day = task.deadline - timedelta(days=1)
            schedule_task(task_id, previous_day.strftime("%Y-%m-%d %H:%M:%S"))
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "task_form.html", {"form": form})

def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect("task_list")

def mark_completed(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.status = "completed"
    task.save()
    return redirect("task_list")

def update_task_status(request, task_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            checked = data.get("checked")
            task = Task.objects.get(id=task_id)
            if checked:
                task.status = "completed"
            else:
                task.status = "pending"
            task.save()
            return JsonResponse({"status": task.get_status_display()})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "任务不存在"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
    return JsonResponse({"success": False, "error": "无效请求"}, status=400)
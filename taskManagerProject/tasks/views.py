from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.utils import timezone
# Create your views here.


def home(request):
    return render(request, 'home.html')


def tasks(request):
    current = Task.objects.filter(user=request.user, completeDate__isnull=True)
    completed = Task.objects.filter(
        user=request.user, completeDate__isnull=False)
    return render(request, 'tasks.html', {'current': current, 'completed': completed})


def create(request):
    if request.method == 'GET':
        return render(request, 'create.html', {'form': TaskForm()})
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
        else:
            error = 'Something went wrong. Try again.'
            return render(request, 'create.html', {'form': TaskForm(), 'error': error})


def detail(request, taskId):
    task = get_object_or_404(Task, id=taskId)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'detail.html', {'task': task, 'form': form})
    else:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
        else:
            error = 'Something went wrong. Try again.'
            form = TaskForm(instance=task)
            return render(request, 'detail.html', {'task': task, 'form': form, 'error': error})


def deleteTask(request, taskId):
    task = get_object_or_404(Task, id=taskId)
    task.delete()
    return redirect('tasks')


def complete(request, taskId):
    task = get_object_or_404(Task, id=taskId)
    task.completeDate = timezone.now()
    task.save()
    return redirect('tasks')
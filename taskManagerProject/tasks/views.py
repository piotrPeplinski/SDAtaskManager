from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
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
        

def detail(request):
    pass

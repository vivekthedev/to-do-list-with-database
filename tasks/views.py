from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegistration
from django.contrib.auth.models import User
# Create your views here.


@login_required
def home(request):
    tasks = Task.objects.all().filter(user=request.user)
    context = {'tasks': tasks}
    return render(request, 'tasks/index.html', context)


@login_required
def addTask(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user = request.user
        if title not in [None, '']:
            task = Task(title=title, user=user)
            task.save()
            return redirect('/')
    return redirect('/')


@login_required
def removeTask(request, id):
    Task.objects.get(id=id).delete()
    return redirect('/')


@login_required
def unDoneTask(request, id):
    task = Task.objects.get(id=id)
    task.isDone = False
    task.save()
    return redirect('/')


@login_required
def doneTask(request, id):
    task = Task.objects.get(id=id)
    task.isDone = True
    task.save()
    return redirect('/')


def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            error = form.errors.get_json_data()
            print(error)
            key = list(error.keys())[0]
            error = error[key][0]['message']
            form = UserRegistration()
            return render(request, 'registration/signup.html', {'form': form,  'error': error})
    else:
        form = UserRegistration()
        return render(request, 'registration/signup.html', {'form': form, 'error': ''})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.method == 'POST':
            if request.POST['password1'] == request.POST['password2']:
                # Register user
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1'])
                    user.save()
                    login(request, user)
                    return redirect('tasks')
                except IntegrityError:
                    return render(request, 'signup.html', {
                        'form': UserCreationForm(),
                        'error': 'Username already taken. Please choose a different one.'})
            else:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Passwords do not match. Please try again.'})


def tasks(request):
    if request.method == 'GET' and request.user.is_authenticated:
        tasks = Task.objects.filter(
            user=request.user, datecompleted__isnull=True)
        return render(request, 'tasks/tasks.html', {
            'tasks': tasks
        })
    else:
        return redirect('home')


def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })
    else:
        # print(request.POST)
        authenticated_user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if authenticated_user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Invalid username or password. Please try again.'
            })
        else:
            login(request, authenticated_user)
            return redirect('tasks')


def create_task(request):
    if request.method == 'GET':
        return render(request, 'tasks/create_task.html', {
            'form': TaskForm()
        })
    else:
        # print(request.POST)
        if request.method == 'POST':
            try:
                form = TaskForm(request.POST)
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('tasks')
            except ValueError:
                return render(request, 'tasks/create_task.html', {
                    'form': TaskForm(),
                    'error': 'Bad data passed in. Please try again.'
                })


def tasks_details(request, task_id):
    if request.method == 'GET' and request.user.is_authenticated:
        task = get_object_or_404(Task, pk=task_id, user=request.user) 
        #task = Task.objects.get(pk=task_id, user=request.user)
        return render(request, 'tasks/tasks_details.html', {
            'task': task
        })
    else:
        return redirect('home')

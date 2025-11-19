from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
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
    return render(request, 'tasks/tasks.html')


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
        print(request.POST)
        return render(request, 'tasks/create_task.html', {
            'form': TaskForm()
        })

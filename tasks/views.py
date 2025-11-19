from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.db import IntegrityError
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
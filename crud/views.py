from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView


# class CustomLoginView(LoginView):
#     def get(self, request, *args, **kwargs):
#         # Check if 'next' parameter exists and points to the login page
#         next_url = request.GET.get('next', '')
#         if next_url and next_url.endswith('/login/'):
#             return redirect('signup')  # Redirect to signup page if 'next' points to login page
#         return super().get(request, *args, **kwargs)

def logouts(request):
    auth_logout(request)
    return redirect('logout_success')  # Redirect to logout success page

def logout_success(request):
    return render(request, 'registration/logout_success.html')
@never_cache
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the user after successful signup
            return redirect('task_list')  # Redirect to task list page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
@never_cache
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('task_list')  # Redirect to task list page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@never_cache
@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'task_manager/task_list.html', {'tasks': tasks})
@never_cache
@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_to = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_manager/task_form.html', {'form': form})

@never_cache
@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_manager/task_form.html', {'form': form})


@never_cache
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_manager/task_confirm_delete.html', {'task': task})

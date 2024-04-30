from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task,Category,UniqueLink
from .forms import TaskForm,TaskFilterForm

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login

from django.contrib.auth import logout as auth_logout
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import LoginView
from django.db.models import Q
from datetime import datetime
from django.http import HttpResponseBadRequest,HttpResponse
import uuid


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


# @never_cache
# @login_required
# def task_list(request):
#     tasks = Task.objects.filter(assigned_to=request.user)
#     return render(request, 'task_manager/task_list.html', {'tasks': tasks})
@login_required
def task_list(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    form = TaskFilterForm(request.GET)

    if form.is_valid():
        category = form.cleaned_data.get('category')
        progress = form.cleaned_data.get('progress')
        status = form.cleaned_data.get('status')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        if category:
            tasks = tasks.filter(category=category)
        if progress:
            tasks = tasks.filter(progress=progress)
        if status:
            tasks = tasks.filter(status=status)
        if start_date:
            tasks = tasks.filter(due_date__gte=start_date)
        if end_date:
            tasks = tasks.filter(due_date__lte=end_date)

    return render(request, 'task_manager/task_list.html', {'tasks': tasks, 'form': form})

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


@login_required

def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'task_manager/task_detail.html', {'task': task})



@login_required
def generate_unique_link(request, pk, permission):
    task = get_object_or_404(Task, pk=pk)
    if permission not in ['view', 'edit', 'admin']:
        return HttpResponseBadRequest("Invalid permission level")

    # Generate a unique URL (you may use UUID or any other method)
    url = 'http://example.com/' + str(uuid.uuid4())

    # Save the unique link to the database
    unique_link = UniqueLink.objects.create(url=url, task=task, permission=permission, creator=request.user)

    return HttpResponse(f"Unique link created: {unique_link.url}")


def handle_unique_link(request, url):
    unique_link = get_object_or_404(UniqueLink, url=url)
    task = unique_link.task
    permission = unique_link.permission

    # Check permissions
    if permission == 'view':
        # Render template for viewing task
        return render(request, 'task_url/task_view_template.html', {'task': task})
    elif permission == 'edit':
        # Render template for editing task
        return render(request, 'task_url/task_edit_template.html', {'task': task})
    elif permission == 'admin':
        # Render template for admin actions
        return render(request, 'task_url/task_admin_template.html', {'task': task})
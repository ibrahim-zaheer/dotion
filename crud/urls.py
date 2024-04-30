from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.signup, name='signup'),
    path('task_list/', views.task_list, name='task_list'),
    path('task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/update/', views.task_update, name='task_update'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logouts, name='logout'),  # URL pattern for logout
    path('logout_success/', views.logout_success, name='logout_success'),  # Optional: URL for logout success page
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('tasks/', views.task_list, name='task_list'),
    #for generating permission links
    path('tasks/<int:pk>/permission/<str:permission>',views.generate_unique_link,name="generate_unique_link"),
   path('task/view/<path:url>/', views.handle_unique_link, name="handle_unique_link")


    
]

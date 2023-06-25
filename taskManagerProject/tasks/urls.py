from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.tasks, name='tasks'),
    path('create/', views.create, name='create'),
    path('tasks/<int:taskId>/', views.detail, name='detail'),
    path('tasks/<int:taskId>/delete/', views.deleteTask, name='deleteTask'),
    path('tasks/<int:taskId>/complete/', views.complete, name='complete'),
]

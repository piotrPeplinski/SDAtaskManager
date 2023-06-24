from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.logUser, name='logUser'),
    path('logout/', views.logoutUser, name='logoutUser'),
]
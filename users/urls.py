from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('home/', views.user_home, name='user_home'),
    path('logout/', views.user_logout, name='user_logout'),
]

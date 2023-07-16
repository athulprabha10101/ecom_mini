from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('', views.user_home, name='user_home'),
    path('logout/', views.user_logout, name='user_logout'),
    path('product/<int:id>', views.user_product, name='user_product'),
    path('cat_product/<int:id>', views.cat_product, name='cat_product'),
    path('otpValidator/', views.otpValidator, name='otpValidator'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('add_address', views.add_address, name='add_address'),
    path('edit_address/<int:id>', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
]

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
    path('user_address', views.user_address, name='user_address'),
    path('user_orders', views.user_orders, name='user_orders'),
    path('add_address', views.add_address, name='add_address'),
    path('edit_address/<int:id>', views.edit_address, name='edit_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('edit_details/<int:id>', views.edit_details, name='edit_details'),
    path('display_cart', views.display_cart, name='display_cart'),
    path('add_to_cart<int:id>', views.add_to_cart, name='add_to_cart'),
    path('add_qty<int:id>', views.add_qty, name='add_qty'),
    path('less_qty<int:id>', views.less_qty, name='less_qty'),
    path('checkout<int:cart_id>', views.checkout, name='checkout'),
    path('remove_item<int:id>', views.remove_item, name='remove_item'),
    path('place_order', views.place_order, name='place_order'),
    path('cancel_req<int:id>', views.cancel_req, name='cancel_req'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('new_password_for_forgotten_password', views.new_password_for_forgotten_password, name='new_password_for_forgotten_password'),
    path('change_password', views.change_password, name='change_password'),
    path('apply_coupon', views.apply_coupon, name='apply_coupon'),

    
    
    
]

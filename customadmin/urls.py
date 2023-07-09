from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.admin_login, name="admin_login"),
    path('logout', views.admin_logout, name="admin_logout"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('block_user/<int:id>', views.block_user, name='block_user'),
    path('categories', views.categories, name="categories"),
    path('add_categories', views.add_categories, name="add_categories"),
    path('edit_categories/<int:id>', views.edit_categories, name="edit_categories"),
    path('delete_categories/<int:id>', views.delete_categories, name="delete_categories"),
    path('products', views.products, name="products"),
    path('add_products', views.add_products, name="add_products"),
]

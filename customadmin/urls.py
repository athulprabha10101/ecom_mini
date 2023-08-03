from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.admin_login, name="admin_login"),
    path('logout', views.admin_logout, name="admin_logout"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('block_user/<int:id>', views.block_user, name='block_user'),
    path('categories', views.categories, name="categories"),
    path('add_categories', views.add_categories, name="add_categories"),
    path('edit_categories/<int:id>', views.edit_categories, name="edit_categories"),
    path('delete_categories/<int:id>', views.delete_categories, name="delete_categories"),
    path('products', views.products, name="products"),
    path('add_products', views.add_products, name="add_products"),
    path('add_variants', views.add_variants, name="add_variants"),
    path('edit_variants/<int:id>', views.edit_variants, name="edit_variants"),
    path('delete_variants/<int:id>', views.delete_variants, name="delete_variants"),
    path('edit_products/<int:id>', views.edit_products, name="edit_products"),
    # path('delete_products/<int:id>', views.delete_products, name="delete_products"), # products = variant
    path('delete_image/<int:id>', views.delete_image, name="delete_image"),
    path('add_image/<int:id>', views.add_image, name="add_image"),
    path('orders', views.orders, name="orders"),
    path('order_details/<int:id>', views.order_details, name="order_details"),
    path('update_item_status/<int:id>', views.update_item_status, name="update_item_status"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
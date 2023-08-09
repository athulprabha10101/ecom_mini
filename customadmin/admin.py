from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(BaseProducts)
admin.site.register(Variations)
admin.site.register(VariantImages)
admin.site.register(Variants)
admin.site.register(UserProfile)
admin.site.register(UserAddress)
admin.site.register(AdminProfile)
admin.site.register(Coupons)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(UsedCoupons)



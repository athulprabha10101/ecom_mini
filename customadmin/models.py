import datetime
from django.db import models
import random
import string
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    image = models.ImageField(upload_to='category')

class BaseProducts(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    has_variant = models.BooleanField(default=False)

class Variations(models.Model):
    product = models.ForeignKey(BaseProducts, on_delete=models.CASCADE, related_name='variations')
    color = models.CharField(max_length=50, null=True, blank=True)

class VariantImages(models.Model):
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE, related_name='variant_images')
    image = models.ImageField(upload_to='product_images')

class Variants(models.Model):
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE, related_name='variants')
    product = models.ForeignKey(BaseProducts, on_delete=models.CASCADE, related_name='variant')
    variantname = models.CharField(max_length=255)
    quantity = models.IntegerField()
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name

class UserAddress(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='addresses')
    address_line1 = models.CharField(max_length=200)
    address_line2 = models.CharField(max_length=200)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    pin = models.CharField(max_length=30)
    default = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

class Coupons(models.Model):
    coupon_code = models.CharField(max_length=8, unique=True)
    coupon_type_choices = (
        ('fixed_amount', 'Fixed Amount'),
        ('percentage', 'Percentage'),
    )
    coupon_type = models.CharField(max_length=50, choices=coupon_type_choices, null=True, blank=True)
    min_spend = models.PositiveIntegerField()
    coupon_discount_percent = models.PositiveIntegerField(null=True, blank=True)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField()
    is_active=models.BooleanField(default=True)

class UsedCoupons(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='coupons_used')
    coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='wishlist_of_user')

class WishItems(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_items')
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE)

    
class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart_of_user')
    applied_coupon = models.ForeignKey(Coupons, on_delete=models.CASCADE, null=True, blank=True)


    @property
    def totalprice(self):
        total = 0
        for item in self.cart_items.all():
            total += item.item.selling_price * Decimal(item.quantity)
        return total

    @property
    def coupon_price(self):
        if self.applied_coupon:
            if self.applied_coupon.coupon_type == 'percentage':
                if self.totalprice >= self.applied_coupon.min_spend:
                    discount = (self.totalprice * (Decimal(self.applied_coupon.coupon_discount_percent))/100)
                    max_discount = self.applied_coupon.max_discount
                    amount = self.totalprice - min(discount, max_discount)
                    return round(amount,2)
                return {'message': "Coupon not applicable on this order. Plesae read t&c ... "}
                    
                
            if self.applied_coupon.coupon_type == 'fixed_amount':
                if self.totalprice >= self.applied_coupon.min_spend:
                    amount = self.totalprice - self.applied_coupon.max_discount
                    return amount
                return {'message': "Coupon not applicable on this order. Plesae read t&c ... "}
        return 0
    
    @property
    def saved_amount(self):
        if self.applied_coupon:
            savings = Decimal(self.totalprice) - Decimal(self.coupon_price)
            savings = savings
            print(savings,"------------savings--------------")
            return round(savings,2)
        return Decimal('0.00')
            
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Variants, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
       return self.item.selling_price * Decimal(self.quantity)

class Orders(models.Model):
    
    payment_choices = (
        ('card', 'Debit/Credit card'),
        ('cod', 'Cash on delivery'),
        ('net_banking', 'Internet Banking'),
        ('upi', 'Pay using UPI app')
    )
    order_status_choices = (
        ('processing', 'Procrssing'),
        ('complete', 'Complete'),
        ('shipped', 'Shipped'),
        ('pending', 'Pending'),
    )

    def generate_ordernum():
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(10))
    
    order_num = models.CharField(max_length=20, default =generate_ordernum)
    applied_coupon = models.ForeignKey(Coupons ,on_delete=models.SET_NULL,null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='orders_of_user')
    order_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=100, choices=payment_choices, default='Cash on delivery')
    order_status = models.CharField(max_length=100, choices=order_status_choices, default='Procrssing')
    order_total_price = models.PositiveIntegerField(default=0)
    coupon_discount = models.PositiveIntegerField(null=True, blank =True)
    
class OrderItems(models.Model):

    item_status_choices = (
        ('Processing','Processing'),
        ('Delivered','Delivered'),
        ('Out of delivery','Out of delivery'),
        ('Cancelled','Cancelled'),
        ('Shipped','Shipped'),
        ('Pending','Pending'),
    )
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='items_in_order')
    item = models.ForeignKey(Variants, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sold_at_price = models.PositiveIntegerField()
    cancel_req = models.BooleanField(default=False)
    cancel_date = models.DateTimeField(blank=True, null=True)
    item_order_status = models.CharField(max_length=100, choices=item_status_choices, default='Procrssing')

    @property
    def ordered_price(self):
        return self.item.selling_price * Decimal(self.quantity)
    


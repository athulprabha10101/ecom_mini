from django.db import models
import random
import string

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

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    @property
    def totalprice(self):
        total = 0
        for item in self.cart_items.all():
            total += item.item.selling_price * item.quantity
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item = models.ForeignKey(Variants, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
       return self.item.selling_price * self.quantity

class Orders(models.Model):
    
    payment_choices = (
        ('card', 'Debit/Credit card'),
        ('cod', 'Cash on delivery'),
        ('net_banking', 'Internet Banking'),
        ('upi', 'Pay using UPI app')
    )
    order_status_choices = (
        ('processing', 'Procrssing'),
        ('delivered', 'Delivered'),
        ('out', 'Out of delivery'),
        ('cancelled', 'Cancelled'),
        ('delivered', 'Delivered'),
        ('shipped', 'Shipped'),
        ('pending', 'Pending'),
    )
    def generate_orderId(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(10))
    
    order_num = models.CharField(max_length=20, default=generate_orderId)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    payment_type = models.CharField(max_length=100, choices=payment_choices, default='Cash on delivery')
    order_status = models.CharField(max_length=100, choices=order_status_choices, default='Procrssing')
    
class Order_items(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Variants, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_price = models.PositiveIntegerField()

    @property
    def ordered_price(self):
        return self.item.selling_price * self.quantity
    

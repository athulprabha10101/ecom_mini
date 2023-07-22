from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    image = models.ImageField(upload_to='category')

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    has_variant = models.BooleanField(default=False)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    color = models.CharField(max_length=50, null=True, blank=True)
    storage = models.CharField(max_length=50, null=True, blank=True)

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    color = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True, related_name='color_images')
    image = models.ImageField(upload_to='product_images')

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    color = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True, related_name='color_variants')
    storage = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True, related_name='storage_variants')
    price = models.DecimalField(max_digits=10, decimal_places=2)
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
    deleted = models.BooleanField(default=False)

    
class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

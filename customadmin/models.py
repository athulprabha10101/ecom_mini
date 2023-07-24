from django.db import models

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
    storage = models.CharField(max_length=50, null=True, blank=True)

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
    deleted = models.BooleanField(default=False)

    
class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

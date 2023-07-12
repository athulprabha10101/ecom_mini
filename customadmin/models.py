from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    image = models.ImageField(upload_to='category')

class Products(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False)
    original_price = models.FloatField(null=False, blank=False)
    selling_price = models.FloatField(null=False, blank = False)
    description = models.TextField(null=False, blank=False)
    is_deleted = models.BooleanField(default=False)

class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='images')
    product_image = models.ImageField(upload_to='product_images')

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name
    
class AdminProfile(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . models import *
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def admin_login(request):
    if request.method== "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password, is_superuser=1)

        if user is not None:
            login(request, user)
            return redirect('admin_home')
        else:
            return render(request, 'customadmin/login.html', {'error':"Wrong credentials"})
    return render(request, 'customadmin/login.html')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def admin_home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        user_details = User.objects.filter(is_superuser=False)
        return render(request, 'customadmin/homepage.html', {'user_details':user_details})
    return render(request, 'customadmin/login.html')

def block_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser:    
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('admin_home')
    return render(request, 'customadmin/login.html')

def categories(request):
    if request.user.is_authenticated and request.user.is_superuser:    
        cat = Category.objects.all()    
        return render(request, 'customadmin/categories.html',{'cat':cat})
    return render(request, 'customadmin/login.html')

def add_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:       
        if request.method=='POST':
            name = request.POST.get('name')
            image = request.FILES.get('image')

            cat = Category.objects.create(name=name, image=image)
            cat.save()
        return redirect('categories')
    return render(request, 'customadmin/login.html')

def edit_categories(request, id):
    if request.user.is_authenticated and request.user.is_superuser:           
        cat = Category.objects.get(id=id)

        if request.method == "POST":
            name=request.POST.get('name')
            image=request.FILES.get('image')

            cat.name = name
            if image:
                cat.image = image
                cat.save()

        return redirect('categories')
    return render(request, 'customadmin/login.html')

def delete_categories(request, id):
    if request.user.is_authenticated and request.user.is_superuser:           
        cat = Category.objects.get(id=id)
        cat.delete()
        return redirect('categories')
    return render(request, 'customadmin/login.html')
    
def products(request):
    if request.user.is_authenticated and request.user.is_superuser:           
        categories = Category.objects.all()
        products = Products.objects.all()
        return render(request, 'customadmin/products.html', {'products':products,'categories':categories})
    return render(request, 'customadmin/login.html')

def add_products(request):
    if request.user.is_authenticated and request.user.is_superuser:           
        if request.method=='POST':
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            quantity = request.POST.get('quantity')
            original_price = request.POST.get('original_price')
            selling_price = request.POST.get('selling_price')
            description = request.POST.get('description')
            images = request.FILES.getlist('image')
            is_deleted = request.POST.get('is_deleted') == 'True'
            
            category = Category.objects.get(id=category_id)

            product = Products.objects.create(
                category=category,
                name=name,
                quantity=quantity,
                original_price=original_price,
                selling_price=selling_price,
                description=description,
                is_deleted = is_deleted  # Set the is_deleted field
            )
            product.save()

            for image in images:
                ProductImage.objects.create(product=product, product_image=image)

            return redirect('products')
    return render(request, 'customadmin/login.html')
    
def edit_products(request, id):
    
    if request.user.is_authenticated and request.user.is_superuser:           
        product = Products.objects.get(id=id)
        
        if request.method == 'POST':
            category_id = request.POST.get('category')
            name = request.POST.get('name')
            quantity = request.POST.get('quantity')
            original_price = request.POST.get('original_price')
            selling_price = request.POST.get('selling_price')
            description = request.POST.get('description')
            is_deleted = request.POST.get('is_deleted') == 'True'

            category = Category.objects.get(id=category_id)
        
            product.category = category
            product.name = name
            product.quantity = quantity
            product.original_price = original_price
            product.selling_price = selling_price
            product.description = description
            product.is_deleted = is_deleted  # Set the is_deleted field
            product.save()
            
            return redirect('products')
        
    return render(request, 'customadmin/login.html')




def delete_products(request, id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect('products')

def delete_image(request, id):
    image = ProductImage.objects.get(id=id)
    image.delete()
    return redirect('products')
        
def add_image(request, id):

    if request.method=='POST':
        images = request.FILES.getlist('image')

        product = Products.objects.get(id=id)

        for image in images:
            ProductImage.objects.create(product=product, product_image=image)
    
        return redirect('products')
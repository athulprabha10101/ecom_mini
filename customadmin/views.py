from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . models import *
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def admin_login(request): 
    if 'name' in request.session:
        return redirect('admin_home')
    if request.method== "POST":
        name = request.POST['name']
        password = request.POST['password']

        print(name)
        print(password)

        try:
            admin = AdminProfile.objects.get(name=name, password=password)
            print(admin)
            if admin:
                request.session['name']= name
                return render(request, 'customadmin/homepage.html')
        except AdminProfile.DoesNotExist:
            
            return render(request, 'customadmin/login.html',{'message':"Wrong credentials"})
        
    return render(request, 'customadmin/login.html')

def admin_logout(request):
    if 'name' in request.session:
        del request.session['name']
    return redirect('admin_login')

def admin_home(request):
    if 'name' in request.session:
        user_details = UserProfile.objects.all()
        return render(request, 'customadmin/homepage.html', {'user_details':user_details})
    return render(request, 'customadmin/login.html')

def block_user(request, id):
    if 'name' in request.session:
        user = UserProfile.objects.get(id=id)
        if user.is_active:
            user.is_active = False
            user.save()
        else:
            user.is_active = True
            user.save()
        return redirect('admin_home')
    return render(request, 'customadmin/login.html')

def categories(request):
    if 'name' in request.session:   
        cat = Category.objects.all()    
        return render(request, 'customadmin/categories.html',{'cat':cat})
    return render(request, 'customadmin/login.html')

def add_categories(request):
    if 'name' in request.session:
        if request.method=='POST':
            name = request.POST.get('name')
            image = request.FILES.get('image')

            cat = Category.objects.create(name=name, image=image)
            cat.save()
        return redirect('categories')
    return render(request, 'customadmin/login.html')

def edit_categories(request, id):
    if 'name' in request.session:
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
    if 'name' in request.session:
        cat = Category.objects.get(id=id)
        cat.delete()
        return redirect('categories')
    return render(request, 'customadmin/login.html')
    
def products(request):
    if 'name' in request.session:
        categories = Category.objects.all()
        variants = Variants.objects.all()
        return render(request, 'customadmin/products.html', {'variants':variants,'categories':categories})
    return render(request, 'customadmin/login.html')

def add_products(request):
    if 'name' in request.session:
        if request.method=='POST':
            category_id = request.POST.get('category')
            baseProductName = request.POST.get('baseProductName')
            hasVariant = request.POST.get('hasVariant')
            variantName = request.POST.get('variantName')
            variantColor = request.POST.get('variantColor')
            variantStorage = request.POST.get('variantStorage')
            variantPrice = request.POST.get('variantPrice')
            variantQuantity = request.POST.get('variantQuantity')
            variantOriginalPrice = request.POST.get('variantOriginalPrice')
            variantSellingPrice = request.POST.get('variantSellingPrice')
            variantDescription = request.POST.get('variantDescription')
            variantImages = request.FILES.getlist('variantImage')
            
            category = Category.objects.get(id=category_id)

            try:
                product = BaseProducts.objects.get(name = baseProductName, category=category)
            except BaseProducts.DoesNotExist:
                product = BaseProducts.objects.create(name=baseProductName, category=category, has_variant=True)

            if hasVariant:
                variation = Variations.objects.get_or_create(product=product, color=variantColor, storage=variantStorage)[0]
            else:
                variation = Variations.objects.get_or_create(product=product, color=None, storage=None)[0]

            variant = Variants.objects.create(
                variation = variation,
                product=product,
                variantname = variantName,
                quantity = variantQuantity,
                original_price = variantOriginalPrice,
                selling_price = variantSellingPrice,
                description = variantDescription,
                is_deleted = False
            )

            for image in variantImages:
                VariantImages.objects.create(variation=variation, image=image)

            return redirect('products')
            
    return render(request, 'customadmin/login.html')

    
def edit_products(request, id):
    
    if 'name' in request.session:
        product = Variants.objects.get(id=id)
        
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
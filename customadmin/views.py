from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from customadmin.models import *
# Create your views here.
from django.contrib.auth.models import User
from django.urls import reverse

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
        variants = Variants.objects.prefetch_related('variation__variant_images').all()
        categories = Category.objects.all()
        existingBaseProducts = BaseProducts.objects.all()

        return render(request, 'customadmin/products.html', 
                      {'variants':variants,
                       'categories':categories,
                       'existingBaseProducts':existingBaseProducts,
                       }
                      )
    return render(request, 'customadmin/login.html')

def add_products(request):
    if 'name' in request.session:
        if request.method=='POST':
            category_id= request.POST.get('category')
            baseProductName = request.POST.get('newProductName')
            has_variant = request.POST.get('hasVariant')=='True'

            category = Category.objects.get(id=category_id)

            if BaseProducts.objects.filter(name=baseProductName, category=category).exists():
                message = "Product already exists!"
            else:
                BaseProducts.objects.create(name=baseProductName, category=category, has_variant=has_variant)
                message = "Product created successfully!"
                messages.success(request, message)
            
            return redirect('products')

    return render(request, 'customadmin/login.html')


def add_variants(request):
    if 'name' in request.session:
        if request.method=='POST':
            baseProduct_id = request.POST.get('baseProduct')
            variantName = request.POST.get('variantName')
            variantColor = request.POST.get('variantColor')
            # variantStorage = request.POST.get('variantStorage')
            variantQuantity = request.POST.get('variantQuantity')
            variantOriginalPrice = request.POST.get('variantOriginalPrice')
            variantSellingPrice = request.POST.get('variantSellingPrice')
            variantDescription = request.POST.get('variantDescription')
            variantImages = request.FILES.getlist('variantImage')
            
            product = BaseProducts.objects.get(id=baseProduct_id)

           
            if variantColor:
                variation, created = Variations.objects.get_or_create(product=product, color=variantColor)
            else:
                variation, created = Variations.objects.get_or_create(product=product)

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

def edit_variants(request, id):
    if 'name' in request.session:
        
        variant = Variants.objects.get(id=id)

        if request.method=='POST':

            product_id = request.POST.get('productCategory')
            variantName = request.POST.get('variantName')
            variantColor = request.POST.get('variantColor')
            # variantStorage = request.POST.get('variantStorage')
            variantQuantity = request.POST.get('variantQuantity')
            variantOriginalPrice = request.POST.get('variantOriginalPrice')
            variantSellingPrice = request.POST.get('variantSellingPrice')
            variantDescription = request.POST.get('variantDescription')
            variantIsDeleted = request.POST.get('variantIsDeleted') == 'True'
            
            product = BaseProducts.objects.get(id=product_id)
            
            # if variantColor and variantStorage:
            #     variation, created = Variations.objects.get_or_create(product=product, color=variantColor, storage=variantStorage)
            if variantColor:
                variation, created = Variations.objects.get_or_create(product=product, color=variantColor)
            # elif variantStorage:
            #     variation, created = Variations.objects.get_or_create(product=product,color=None, storage=variantStorage)
            else:
                variation, created = Variations.objects.get_or_create(product=product)
            
            variant.product = product
            variant.variation = variation
            variant.variantname = variantName
            variant.quantity = variantQuantity
            variant.original_price = variantOriginalPrice
            variant.selling_price = variantSellingPrice
            variant.description = variantDescription
            variant.is_deleted = variantIsDeleted
            variant.save()
            

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

# def delete_products(request, id):
#     product = Products.objects.get(id=id)
#     product.delete()
#     return redirect('products')

def delete_variants(request, id):
    variant = Variants.objects.get(id=id)
    variant.is_deleted=True
    variant.save()
    return redirect('products')

def delete_image(request, id):
    image = VariantImages.objects.get(id=id)
    image.delete()
    return redirect('products')
        
def add_image(request, id):

    if request.method=='POST':
        images = request.FILES.getlist('image')
        variant = Variants.objects.get(id=id)

        for image in images:
            VariantImages.objects.create(variation = variant.variation, image=image)
    
        return redirect('products')
    
def orders(request):
    
    if 'name' in request.session:
        
        orders = Orders.objects.all().prefetch_related('items_in_order')

        return render(request, 'customadmin/orders.html', {'orders': orders})
        
    return render(request, 'customadmin/login.html')


def order_details(request, id):

    if 'name' in request.session:

        order = Orders.objects.get(id=id)
        order_details = OrderItems.objects.filter(order=order)

        return render(request, 'customadmin/order_details.html', {'order_details': order_details, 'order':order})

    return render(request, 'customadmin/login.html')


def update_item_status(request, id):

    if 'name' in request.session:

        if request.method == 'POST':
            orderitem = OrderItems.objects.get(id=id)
            status = request.POST['item_status']
            print(status,"------------------>>")
            print(orderitem.item.variantname,"------------------>>")
            
            orderitem.item_order_status = status
            
            
            if status == 'Cancelled':
                orderitem.cancel_date = timezone.now()
                print("cancel------------------>>")
                
            
            orderitem.save()
            print("saved------------------>>")

            return redirect('order_details', id=id)
            

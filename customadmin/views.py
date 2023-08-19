from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from customadmin.models import *
# Create your views here.
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Sum, F
from datetime import datetime, timedelta


from datetime import datetime, timedelta
from django.utils import timezone
from random import choice, randint
from django import forms

from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from io import BytesIO

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

def admin_dashboard(request):
    if 'name' in request.session:
        
        return render(request, 'customadmin/dashboard.html')
    return render(request, 'customadmin/login.html')


def orders_chart_data(request):
    today = datetime.now()
    start_date = today - timedelta(days=3 * 365)
    
    monthly_data = Orders.objects.filter(order_date__year__gte=start_date.year).values('order_date__month').annotate(total=Sum('order_total_price'))
    yearly_data = Orders.objects.filter(order_date__year__gte=start_date.year).values('order_date__year').annotate(total=Sum('order_total_price'))
    weekly_data = Orders.objects.filter(order_date__gte=start_date).annotate(week_number=F('order_date__week')).values('week_number').annotate(total=Sum('order_total_price'))


    # Create data arrays for chart
    monthly_orders = [0] * 12
    for entry in monthly_data:
        monthly_orders[entry['order_date__month'] - 1] = entry['total']

    yearly_orders = [0] * (today.year - Orders.objects.earliest('order_date').order_date.year + 1)
    for entry in yearly_data:
        yearly_orders[entry['order_date__year'] - Orders.objects.earliest('order_date').order_date.year] = entry['total']

    weekly_orders = [0] * 52
    for entry in weekly_data:
        week_number = entry['week_number'] - 1  
        weekly_orders[week_number] = entry['total']

    data = {
        'monthly_orders': monthly_orders,
        'yearly_orders': yearly_orders,
        'weekly_orders': weekly_orders,
        'yearly_orders_start_year': Orders.objects.earliest('order_date').order_date.year,
    }

    return JsonResponse(data)


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
                orderitem.item_order_status = 'Cancelled'
                orderitem.cancel_date = timezone.now()
                
                
                print("cancel------------------>>")
                
            
            orderitem.save()
            print("saved------------------>>")

            return redirect('order_details', id=id)

def coupons(request):
    
    if 'name' in request.session:
        
        coupons = Coupons.objects.all()

        return render(request, 'customadmin/coupons.html', {'coupons': coupons})
        
    return render(request, 'customadmin/login.html')

def deactivate_coupon(request, coupon_id):
    if 'name' in request.session:
        coupon = Coupons.objects.get(id=coupon_id)
        coupon.is_active = False
        coupon.save()
    return redirect()

def add_coupon(request):
    if 'name' in request.session:
        if request.method=='POST':
            couponCode = request.POST['couponCode']
            coupon_type = request.POST['coupon_type']
            min_spend = request.POST['min_spend']
            max_discount = request.POST['max_discount']
            max_discount = request.POST['max_discount']
            coupon_discount_percent = request.POST['coupon_discount_percent']
            expiry_date = request.POST['expiry_date']

        if coupon_type == "fixed_amount":
            coupon = Coupons.objects.create(
              coupon_code = couponCode,
              coupon_type = coupon_type,
              min_spend = min_spend,
              max_discount=max_discount,
              expiry_date=expiry_date
            )

        if coupon_type == "percentage":
            coupon = Coupons.objects.create(
              coupon_code = couponCode,
              coupon_type = coupon_type,
              min_spend = min_spend,
              coupon_discount_percent = coupon_discount_percent,
              max_discount=max_discount,
              expiry_date=expiry_date,
            )
        return redirect('coupons')

def test(request):

    return render(request, 'customadmin/testhtml.html')

def test_func_add_orders(request):
    
    users = UserProfile.objects.exclude(name='GUEST')
    order_status_choices = ['complete']  # Order status is always 'complete'

    
    start_date = timezone.now() - timedelta(days=3 * 365)
    end_date = timezone.now()

    for _ in range(100):  # Generate 100 sample orders
        user = choice(users)
        order_date = start_date + timedelta(
            seconds=randint(0, int((end_date - start_date).total_seconds()))
        )
        print('------------zxczxczxczcxzxxczxcxzczxcxz', order_date)
        order_total_price = randint(10000, 100000)  # Adjust the price range as needed
        
        order = Orders.objects.create(
            user=user,
            order_address=user.addresses.first(),  
            order_date=order_date,
            order_status=choice(order_status_choices),
            order_total_price=order_total_price
        )
        print("orders also generated")

        print("Sample orders generated successfully!")

    return redirect('test')

def generate_sales_report(request):
    
    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

        orders = Orders.objects.filter(order_date__gte=from_date, order_date__lte=to_date)

        total_orders = orders.count()
        total_items = sum(order.items_in_order.aggregate(Sum('quantity'))['quantity__sum'] or 0 for order in orders)
        total_revenue = sum(order.order_total_price for order in orders)


        sales_data = {
            'from_date': from_date_str,
            'to_date': to_date_str,
            'total_orders': total_orders,
            'total_items': total_items,
            'total_revenue': total_revenue,
            'orders': orders,
        }
        
        return render(request, 'customadmin/salesreport.html', {'sales_data': sales_data})
    
    return render(request, 'sales_report_form.html')


def generate_sales_report_pdf(request, from_date, to_date):
    from_date_str = from_date
    to_date_str = to_date

    from_date = datetime.strptime(from_date, '%Y-%m-%d')
    to_date = datetime.strptime(to_date, '%Y-%m-%d')

    orders = Orders.objects.filter(order_date__gte=from_date, order_date__lte=to_date)

    total_orders = orders.count()
    total_items = sum(order.items_in_order.aggregate(Sum('quantity'))['quantity__sum'] or 0 for order in orders)
    total_revenue = sum(order.order_total_price for order in orders)

    sales_data = {
        'from_date': from_date_str,
        'to_date': to_date_str,
        'total_orders': total_orders,
        'total_items': total_items,
        'total_revenue': total_revenue,
        'orders': orders,
    }

    template_path = 'customadmin/salesreport_pdf_template.html'  # Path to your HTML template
    context = {'sales_data': sales_data}
    template = get_template(template_path)
    html = template.render(context)
    response = BytesIO()

    pdf_file = 'sales_report.pdf'  # Name of the PDF file
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), response)
    
    if not pdf.err:
        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{pdf_file}"'
        return response
    
    return HttpResponse("Error generating PDF", status=500)

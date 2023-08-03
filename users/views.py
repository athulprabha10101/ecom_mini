import random
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from customadmin.models import *
from twilio.rest import Client
from django.contrib import messages

# Create your views here.
from django.contrib.auth.models import User
import sys
print(sys.path)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sendOtp(otp):
    account_sid = 'ACcf98c3b4a60a5236362474c850a6477d'
    auth_token = '301e25d5ddc49a99ce541375832a38ae'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Your otp is '+otp,
        from_='+13253265322',
        to='+918592808592'
     )
    print(message.sid)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otpValidator(request):
    phone = request.session['userdetails']['phone']
    
    if request.method=="POST":
        
        entered_otp = request.POST['otp']

        if request.session['userdetails']['otp'] == entered_otp:

            userdetails=request.session['userdetails']

            name = userdetails['name']
            email = userdetails['email']
            mobile = userdetails['phone']
            password = userdetails['password']

            UserProfile.objects.create(name=name, email=email, phone=mobile, password=password)

            return redirect('user_login')
        
        return render(request, 'users/register.html', {'error': "OTP Wrong"})
    
    return render(request, 'store/otp_validator.html', {'phone':phone})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        user = UserProfile.objects.filter(email=email).exists()

        if user:
            return render(request, 'users/register.html', {'error': "Email already exists"})
        user = UserProfile.objects.filter(phone=phone).exists()

        if user:
            return render(request, 'users/register.html', {'error': "Phone number already exists"})

        if password == cpassword:

            otp = str(random.randint(1000, 9999))

            #sendOtp(otp)

            print("-----------------------")
            print(otp)
            print("-----------------------")

            request.session['userdetails'] = {
                'name':name,
                'email':email,
                'phone':phone,
                'password':password,
                'otp':otp,
            }
            return redirect('otpValidator')

        else:
            return render(request, 'users/register.html', {'error': "Password mismatch"})

    return render(request, 'users/register.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if 'email' in request.session:
        return redirect('user_home')
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserProfile.objects.get(email=email, password=password)
            if user:
                if not user.is_active:
                    return render(request, 'users/login.html', {'message': "User Blocked"})
                request.session['email'] = email
                return redirect('user_home')

        except UserProfile.DoesNotExist:

            return render(request, 'users/login.html', {'message': "Wrong credentials"})

    return render(request, 'users/login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('user_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_home(request):
    categories = Category.objects.all()

    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])

        return render(request, 'store/homepage.html', {'categories': categories, 'user': user})

    return render(request, 'store/homepage.html', {'categories': categories})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_product(request, id):
    variant = Variants.objects.get(id=id)
    images = variant.variation.variant_images.all()
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/product.html',{'variant': variant, 'images': images, 'user': user})  # Sends a single variant to html
    
    return render(request, 'store/product.html',{'variant': variant, 'images': images, 'user':'none'}) 


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cat_product(request, id):
    cat = Category.objects.get(id=id)
    variants = Variants.objects.filter(product__category=cat)
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/cat_products.html', {'products': variants, 'user': user})
    
    return render(request, 'store/cat_products.html', {'products': variants, 'user':'none'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_profile(request):
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/user_profile.html', {'user':user}) #profile

    return redirect('user_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_address(request):
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/user_address.html', {'user':user}) # address

    return redirect('user_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_orders(request):
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email']) # orders
        orders = Orders.objects.filter(user=user).prefetch_related('items_in_order')
        
        return render(request, 'store/user_orders.html', {'user':user, 'orders':orders})

    return redirect('user_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_address(request):
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email= request.session['email'])

        
        if request.method=='POST':
            
            address_line1 = request.POST['address1']
            address_line2 = request.POST['address2']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            pin = request.POST['pin']
            checkout = request.POST.get('checkout') == 'True'
            # default = request.POST.get() == 'True'

            UserAddress.objects.create(
                user=user, 
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                country=country,
                pin=pin
                )
            if checkout:
                return redirect('checkout')
            return redirect('user_profile')
    
    return redirect('user_login')    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_address(request, id):
    if 'email' in request.session:
        address = UserAddress.objects.get(id=id)

        if request.method=='POST':
            address.address_line1=request.POST['address1']
            address.address_line2=request.POST['address2']
            address.city=request.POST['city']
            address.state=request.POST['state']
            address.country=request.POST['country']
            address.pin=request.POST['pin']
            address.save()
            return redirect('user_profile')
        
    return redirect('user_login')    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_address(request, id):
    if 'email' in request.session:
        address = UserAddress.objects.get(id=id)
        address.deleted=True
        address.save()
        return redirect('user_profile')
    
    return redirect('user_login')    
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_details(request, id):
    if 'email' in request.session and request.method == 'POST':
        user = UserProfile.objects.get(id=id)
        errors = []

        display_name = request.POST.get('displayName', '').strip()
        email = request.POST.get('email', '').strip()
        phonenum = request.POST.get('phonenum', '').strip()
        old_password = request.POST.get('oldPassword', '').strip()
        new_password = request.POST.get('newPassword', '').strip()
        confirm_password = request.POST.get('confirmPassword', '').strip()

        if display_name:
            user.name = display_name
            user.save()

        if email:
            if not UserProfile.objects.filter(email=email).exists():
                user.email = email
                request.session['email'] = email
                user.save()
            else:
                errors.append(f"{email} - email already exists")
                
        
        if phonenum:
            if UserProfile.objects.filter(phone=phonenum).exists():
                errors.append(f"{phonenum} - phone number already exists")
            else:
                user.phone = phonenum
                user.save()

        if old_password and old_password != '' and old_password == user.password and new_password == confirm_password:
            print("----------------------")
            print(request.POST)
            
            user.password = new_password
            user.save()
            print("----------------------")
            print("CHANGED")
        else:
            errors.append("Password mismatch")
            print("mismatch")

        if errors:
            return render(request, 'store/user_profile.html', {'errors': errors, 'user': user})

        
        return render(request, 'store/user_profile.html', {'user':user})

    return redirect('user_login')


def add_to_cart(request, id):
    
    if 'email' in request.session:

        user = UserProfile.objects.get(email=request.session['email'])
        
        if request.method == 'POST':
            variant = Variants.objects.get(id=id)
            cart, created = Cart.objects.get_or_create(user=user)

            try:
                check = cart.cart_items.get(item=variant)
                messages.success(request," already added to cart .... ")    
                return redirect('user_product', id=id)
            except:
                CartItem.objects.create(cart=cart, item=variant, quantity=1)
                messages.success(request," added to cart .... ")
                return redirect('user_product', id=id)
            
    messages.warning(request,"Not logged in ...")
    return redirect('user_login')


def display_cart(request, id=None):
    
    if 'email' in request.session:

        user = UserProfile.objects.get(email = request.session['email'])
        cart, created = Cart.objects.get_or_create(user=user)
        items = cart.cart_items.all()
        
        return render(request, 'store/cart.html', {'user':user, 'items':items, 'cart':cart})
   
    return render(request, 'users/login.html', {'error': "login to see your cart... "})

def remove_item(request, id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    return redirect('display_cart')

def add_qty(request, id):
    cart_item = CartItem.objects.get(id=id)
    if cart_item.quantity < 10:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('display_cart')
    
def less_qty(request, id):
    cart_item = CartItem.objects.get(id=id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return redirect('display_cart')

def checkout(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    addresses = UserAddress.objects.filter(user = cart.user)
    cart_items = cart.cart_items.all()
    
    return render(request, 'store/checkout.html',{'cart_items':cart_items, 'addresses':addresses, 'cart':cart})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    if 'email' in request.session:
        
        if request.method=='POST':
            
            user = UserProfile.objects.get(email=request.session['email'])
            order_address_id = request.POST['order_address_id']
            order_address = UserAddress.objects.get(id=order_address_id)
            cart = Cart.objects.get(user=user)

            current_order = Orders.objects.create(
                    
                    user = user,
                    order_address = order_address,
                )
            items = cart.cart_items.all()
            for item in items:
                OrderItems.objects.create(
                    order = current_order,
                    item = item.item,
                    quantity = item.quantity,
                    sold_at_price = item.item.selling_price
                )
            cart.delete()
            order_num = current_order.order_num
            return render(request, 'store/success.html', {'order_num':order_num})
    return render(request, 'users/login.html', {'error': 'login to purchase'})

def cancel_req(request, id):
    print(id, "-----------------------------HELLO ID")
    item = OrderItems.objects.get(id=id)
    item.cancel_req = True
    item.save()
    return redirect(user_orders)
    
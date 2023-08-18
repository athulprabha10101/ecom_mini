import random
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control
from customadmin.models import *
from twilio.rest import Client
from django.contrib import messages
import razorpay
from django.conf import settings
# Create your views here.
from django.contrib.auth.models import User
import sys
from django.db import transaction
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

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

def forgot_password(request):
    return render(request, 'users/forgot_password.html')

def new_password_for_forgotten_password(request):
    
    if request.method=='POST':
        email = request.POST['email']
        phone_num = request.POST['phone']

        try:
            user = UserProfile.objects.get(phone=phone_num, email=email)
            if user:
                generatedotp = str(random.randint(1000, 9999))
                
                print("-------------OTP FOR PASSWORD CHANGE-------------")
                print("---------------",generatedotp)
                print("-------------OTP FOR PASSWORD CHANGE-------------")

                request.session['newPasswordOTP'] = {
                    'generatedotp':generatedotp,
                    'user_id':user.id,
                }

                return render(request, 'users/set_new_password.html')
            
        except UserProfile.DoesNotExist:
            return render(request, 'users/forgot_password.html',{'invalid':"Invalid credentials, try again"})

@cache_control(no_cache=True, must_revalidate=True)
def change_password(request):

    if request.method == 'POST':
        enteredOTP = request.POST['enteredOTP']
        newpassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']

        generatedOTP = request.session['newPasswordOTP']['generatedotp']
        user = UserProfile.objects.get(id=request.session['newPasswordOTP']['user_id'])

        if confirmPassword == newpassword:
            if  generatedOTP== enteredOTP:                
                user.password = newpassword
                user.save()                
                request.session.flush()

                return redirect('user_login') # when this is 'rendered' with context instead of redirect, throws enteredOTP multivaluedictkey error
            
        return render(request, 'users/set_new_password.html',{'error':'Passwords / OTP not matching'})
        
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
        user = UserProfile.objects.get(email=request.session['email']) 
        orders = Orders.objects.filter(user=user).prefetch_related('items_in_order')
        historical_addresses = OrderAddressHistory.objects.filter(order__in=orders)

        return render(request, 'store/user_orders.html', {'user':user, 'orders':orders, 'historical_address':historical_addresses})

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
            checkout = request.POST['checkout'] == 'True'
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
                return redirect('checkout',cart_id=user.cart_of_user.id)
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
            images = variant.variation.variant_images.all()
            cart, created = Cart.objects.get_or_create(user=user)

            try:
                check = cart.cart_items.get(item=variant)
                toast_already_added = "Already added to cart"
                return render(request, 'store/product.html',{'variant':variant,'images': images, 'user': user, 'toast_already_added':toast_already_added })
            except:
                CartItem.objects.create(cart=cart, item=variant, quantity=1)
                toast_added = "Added to cart"
                return render(request, 'store/product.html',{'variant':variant,'images': images, 'user': user, 'toast_added':toast_added })
            

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
    
    user = UserProfile.objects.get(email = request.session['email'])
    cart = Cart.objects.get(user=user)
    coupon = cart.applied_coupon
    items = cart.cart_items.all()

    if coupon and coupon.min_spend > cart.totalprice:
        cart.applied_coupon = None
        return render(request, 'store/cart.html', {'user': user,'items':items, 'cart':cart,'message': f"Coupon reoved. Minimum purchase is: {coupon.minspend}"})

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
    coupon = cart.applied_coupon

    client = razorpay.Client(auth=(settings.RAZOR_KEY, settings.KEY_SECRET))

    if not coupon:
        payment = client.order.create({'amount':float(cart.totalprice*100), 'currency':'INR', 'payment_capture':1})
    else:
        payment = client.order.create({'amount': float(cart.coupon_price * 100), 'currency': 'INR', 'payment_capture': 1})

    return render(request, 'store/checkout.html',{'cart_items':cart_items, 'coupon':coupon, 'addresses':addresses, 'cart':cart, 'payment':payment})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def place_order(request):
    if 'email' in request.session:
        print("--------order place clicked------------XXXXXXXX")
        if request.method=='POST':

            with transaction.atomic():
                selected_payment_method = request.POST.get('payment_method')  # Get the selected payment method
                user = UserProfile.objects.get(email=request.session['email'])
                order_address_id = request.POST['order_address_id']
                order_address = UserAddress.objects.get(id=order_address_id)
                cart = Cart.objects.get(user=user)
                cart_total_price = cart.totalprice
                

                if cart.applied_coupon:
                    applied_coupon = cart.applied_coupon
                    print(applied_coupon.coupon_code,"--------------------XXXXXXXX")

                    current_order = Orders.objects.create(
                        user = user,
                        order_address = order_address,
                        applied_coupon = applied_coupon,
                        order_total_price = cart.coupon_price,
                        coupon_discount = cart.saved_amount,
                    )
                    print(current_order,"---------order object created for applied coupon-----------XXXXXXXX")
                    
                    usedcoupon = UsedCoupons.objects.create(
                        user=user,
                        coupon=applied_coupon
                    )
                    print(usedcoupon,"---------attempting usercoupon creation-----------XXXXXXXX"),

                else:
                    current_order = Orders.objects.create(
                        user = user,
                        order_address = order_address,
                        applied_coupon = None,
                        order_total_price = cart.totalprice,
                        coupon_discount = None
                    )

                items = cart.cart_items.all()

                for item in items:
                    OrderItems.objects.create(
                        order = current_order,
                        item = item.item,
                        quantity = item.quantity,
                        sold_at_price = item.item.selling_price
                    )

                if selected_payment_method == 'cod':
                    current_order.payment_type = 'Cash on delivery'
                    current_order.save()

                elif selected_payment_method == 'onlinepayment':
                    current_order.payment_type = 'Internet Banking'
                    current_order.save()
                # more payment methods can be added . as razorpay has all, settling with netbanking for all

                for cart_item in cart.cart_items.all():
                    variant = cart_item.item
                    purchased_quantity = cart_item.quantity
                    variant.quantity -= purchased_quantity
                    variant.save()
                
                address_history = OrderAddressHistory.objects.create(
                        order = current_order,
                        address_line1 = order_address.address_line1,
                        address_line2 = order_address.address_line2,
                        city = order_address.city,
                        state = order_address.state,
                        country = order_address.country,
                        pin = order_address.pin,
                    )

                cart.delete()
                order=current_order
                curent_order_items =order.items_in_order.all()
                
                context = { 'order':order,
                            'items':curent_order_items,
                            'totalprice':cart_total_price, 
                          }
                
                return render(request, 'store/success.html', context)
    return render(request, 'users/login.html', {'error': 'login to purchase'})

def cancel_req(request, id):
    item = OrderItems.objects.get(id=id)
    item.cancel_req = True
    item.save()
    return redirect(user_orders)

def apply_coupon(request):
    if 'email' in request.session:
        if request.method=='POST':
            code = request.POST['code']

            user = UserProfile.objects.get(email=request.session['email'])
            cart = Cart.objects.get(user=user)
            items = cart.cart_items.all()
            used = UsedCoupons.objects.filter(user=user, coupon__coupon_code=code).exists()

            if used:
                return render(request, 'store/cart.html', {'user': user,'items':items, 'cart':cart,'message': str("Coupon expired!")})
     
            else:
                try:
                    coupon = Coupons.objects.get(coupon_code=code)
                    user = UserProfile.objects.get(email = request.session['email'])
                    cart = Cart.objects.get(user=user)
                    items = cart.cart_items.all()
                    cart.applied_coupon = coupon
                    cart.save()
                    print("saved--------------------------")

                    return render(request, 'store/cart.html',{'user':user, 'items':items, 'cart':cart, 'coupon':coupon } )

                except Coupons.DoesNotExist:
                    user = UserProfile.objects.get(email = request.session['email'])
                    cart = Cart.objects.get(user=user)
                    items = cart.cart_items.all()
                    
                    return render(request, 'store/cart.html', {'user':user, 'items':items, 'cart':cart, 'message':"invalid Coupon"})
                    
        return redirect('display_cart')
    return redirect('user_login')

def wishlist(request):
    
    if 'email' in request.session:

        user = UserProfile.objects.get(email = request.session['email'])
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        variants = wishlist.wishlist_items.all()
        
        return render(request, 'store/wishlist.html', {'user':user, 'variants':variants, 'wishlist':wishlist})
   
    return render(request, 'users/login.html', {'error': "login to see your wishlist... "})

def add_to_wishlist(request, id):
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        variant = Variants.objects.get(id=id)
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        images = variant.variation.variant_images.all()

        try:
            check = wishlist.wishlist_items.get(variant=variant)
            toast_already_added = "Already added to wishlist"
            return render(request, 'store/product.html', {
            'variant': variant,
            'images': images,
            'user': user,
            'toast_already_added': toast_already_added
        })
        except:
            WishItems.objects.create(wishlist=wishlist, variant=variant)
            toast_added = "Added to wishlist"
            return render(request, 'store/product.html', {
            'variant': variant,
            'images': images,
            'user': user,
            'toast_added': toast_added
        })

        # Fetch the other necessary data for rendering the product page
        

        

    return redirect('user_login')

def remove_from_wishlist(request, id):
    wishlist_item = WishItems.objects.get(id=id)
    wishlist_item.delete()

    return redirect('wishlist')

def add_to_cart_from_wishlist(request, id,wishlistitem_id):
        user = UserProfile.objects.get(email=request.session['email'])
        variant = Variants.objects.get(id=id)
        cart, created = Cart.objects.get_or_create(user=user)
        

        try:
            check = cart.cart_items.get(item=variant)
            messages.success(request," already added to cart .... ")
            remove_from_wishlist(request,wishlistitem_id)    
            return redirect('display_cart')
        except:
            CartItem.objects.create(cart=cart, item=variant, quantity=1)
            messages.success(request," added to cart .... ")
            remove_from_wishlist(request, wishlistitem_id)
            return redirect('display_cart')
            
def generate_invoice(request, order_id):
    order = Orders.objects.get(id=order_id)
    grand_total = order.order_total_price - (order.coupon_discount or 0)

    template_path = 'pdf/invoice_template.html'

    context = {'order': order, 'grand_total': grand_total}

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="incoice_{order.order_num}.pdf"'
    pisa_status= pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("An error occured")
    return response

def test_func(request):
    message = "toaster working"
    message_b = False
    return render (request, 'store/testhtm.html', {'message':message, 'message_b':message_b})
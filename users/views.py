import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from customadmin.models import *
from twilio.rest import Client

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


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


def user_logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('user_login')


def user_home(request):
    categories = Category.objects.all()

    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])

        return render(request, 'store/index-3.html', {'categories': categories, 'user': user})

    return render(request, 'store/index-3.html', {'categories': categories})


def user_product(request, id):
    product = Products.objects.get(id=id)
    images = product.images.all()
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/product.html',
                    {'product': product, 'images': images, 'user': user})  # Sends a single prod to html
    
    return render(request, 'store/product.html',
                {'product': product, 'images': images, 'user':'none'}) 



def cat_product(request, id):
    cat = Category.objects.get(id=id)
    products = Products.objects.filter(category=cat)
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/cat_products.html', {'products': products, 'user': user})
    
    return render(request, 'store/cat_products.html', {'products': products, 'user':'none'})

def user_profile(request):
    
    if 'email' in request.session:
        user = UserProfile.objects.get(email=request.session['email'])
        return render(request, 'store/user_profile.html', {'user':user})

    return redirect('user_login')

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

            UserAddress.objects.create(
                user=user, 
                address_line1=address_line1,
                address_line2=address_line2,
                city=city,
                state=state,
                country=country,
                pin=pin
                )
            return redirect('user_profile')

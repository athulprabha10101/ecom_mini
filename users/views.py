from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from customadmin.models import *

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def user_register(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            UserProfile.objects.create(name = name, email=email, phone=phone, password=password)

            return redirect('user_login')
        else:
            return render(request, 'users/register.html',{'error':"Password mismatch"})


    return render(request, 'users/register.html')


def user_login(request):
    if 'email' in request.session:
        return redirect ('user_home')
    if request.method== "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserProfile.objects.get(email = email , password = password)
            if user:
                request.session['email'] = email
                return  render(request, 'store/index-3.html', {'user': user})

        except UserProfile.DoesNotExist:

            return render(request, 'users/login.html',{'message':"Wrong credentials"})
        
    return render(request, 'users/login.html')


def user_logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('user_home')

def user_home(request):
    if 'email' in request.session:
        return render(request, 'store/index-3.html')
    
    return redirect('user_login')


    

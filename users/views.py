from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from customadmin.models import *

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def user_register(request):
    if request.method=='POST':
        username = request.POST['username']
        phone = request.POST['phone']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if password == cpassword:
            user = User.objects.create_user(username=username, phone=phone, password=password, is_superuser=0)
            login(request, user)
            return redirect('user_login')
        else:
            return render(request, 'users/register.html',{'error':"Password mismatch"})


    return render(request, 'users/register.html')


def user_login(request):
    if request.method== "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'users/login.html', {'error':"Wrong credentials"})
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def user_home(request):

    return render(request, 'store/index-3.html')

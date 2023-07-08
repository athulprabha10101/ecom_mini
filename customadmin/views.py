from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

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
    return render(request, 'customadmin/home.html')

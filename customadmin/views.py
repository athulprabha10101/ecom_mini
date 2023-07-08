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
    if request.user.is_authenticated and request.user.is_superuser:
        user_details = User.objects.filter(is_superuser=False)
        return render(request, 'customadmin/homepage.html', {'user_details':user_details})    
    return render(request, 'customadmin/login.html')

def block_user(request, id):
    user = User.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('admin_home')

def test(request):
    return render(request, 'customadmin/base.html')

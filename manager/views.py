from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Product


def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def login(request):
    return render(request, 'login.html', {})

def help(request):
    return render(request, 'help.html', {})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def inventory(request):
    products = Product.objects.all()
    return render(request, 'inventory.html', {'products': products})
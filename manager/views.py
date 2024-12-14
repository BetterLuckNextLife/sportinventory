from django.shortcuts import render
from .models import Product

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def login(request):
    return render(request, 'login.html', {})

def help(request):
    return render(request, 'help.html', {})

def register(request):
    return render(request, 'register.html', {})

def inventory(request):
    products = Product.objects.all()
    return render(request, 'inventory.html', {'products': products})
from django.shortcuts import render
from .models import Product

def home(request):
    return render(request, 'index.html', {})

def help(request):
    return render(request, 'help.html', {})

def register(request):
    return render(request, 'register.html', {})

def user(request):
    products = Product.objects.all()
    return render(request, 'user.html', {'products': products})
from django.shortcuts import render

def home(request):
    return render(request, 'index.html', {})

def help(request):
    return render(request, 'help.html', {})

def register(request):
    return render(request, 'register.html', {})

def user(request):
    return render(request, 'user.html', {})


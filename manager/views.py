from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
@login_required
def inventory(request):
    if request.method == "POST":
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        state = request.POST.get('state')

        # Проверка количества
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("Количество должно быть положительным числом.")
        except (ValueError, TypeError):
            messages.error(request, "Некорректное количество! Введите положительное число.")
            return redirect('inventory')

        # Проверяем существующий продукт
        existing_product = Product.objects.filter(name=name, state=state, owner=request.user).first()

        if existing_product:
            existing_product.quantity += quantity
            existing_product.save()
        else:
            Product.objects.create(name=name, quantity=quantity, state=state, owner=request.user)

        messages.success(request, "Элемент успешно добавлен в инвентарь.")
        return redirect('inventory')

    # Получаем продукты пользователя
    products = Product.objects.filter(owner=request.user)
    return render(request, 'inventory.html', {'products': products})
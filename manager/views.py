from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import Product
from django.contrib.auth.decorators import login_required


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
        quantity = int(request.POST.get('quantity', 1))
        state = request.POST.get('state', 'inactive')

        # Проверяем, есть ли такой же продукт с таким же состоянием
        existing_product = Product.objects.filter(
            name=name, state=state, owner=request.user
        ).first()

        if existing_product:
            # Если продукт уже существует, увеличиваем количество
            existing_product.quantity += quantity
            existing_product.save()
        else:
            # Иначе создаём новый продукт
            Product.objects.create(
                name=name,
                quantity=quantity,
                state=state,
                owner=request.user
            )

        return redirect('inventory')

    # Получаем все продукты текущего пользователя
    products = Product.objects.filter(owner=request.user)
    return render(request, 'inventory.html', {'products': products})

from django.shortcuts import render, redirect
from .models import *
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.db.models import Count, F, Q

from .utils import usage_report, db_report


def verified_check(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.verified:
            return view_func(request, *args, **kwargs)
        return redirect('not_verified')  # Правильный редирект по URL name или путь

    return wrapper


def is_admin(user):
    return user.is_staff == True


def error_404_view(request, exception=None):
    return render(request, '404.html', status=404)


@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    if request.method == "POST":
        if "username" in request.POST:
            username = request.POST.get('username')
            verifinguser = User.objects.filter(username=username).first()
            verifinguser.verified = True
            verifinguser.save()
        elif "verification" in request.POST:
            action = request.POST.get("verification")
            identificator = int(request.POST.get("ident"))

            app = Application.objects.filter(ident=identificator).first() # Объект заявки

            if action == "reject": # Удалить если отклняем
                app.delete()
            elif action == "accept": # Если принять, то покупаем нужные вещи или выдаём уже имеющиеся
                prod = Product.objects.filter(
                    name=app.name,
                    owner=app.owner,
                    state=app.state
                ).first()
                print(app.name, app.state, app.owner)
                if prod:
                    if app.action == 'drop' and prod.state != "broken":
                        prod = Product.objects.create(
                        name=app.name,
                        owner=None,
                        state='inactive'
                        )
                        prod.save()
                    elif app.action == 'drop' and prod.state == "broken":
                        if app.quantity <= prod.quantity:
                            prod.quantity -= app.quantity
                    elif app.action == 'request':

                        storageprod = Product.objects.filter(
                                name=app.name,
                                owner=None,
                            ).first()
                        if storageprod:
                            storageprod.quantity -= app.quantity
                            prod.quantity += app.quantity
                        buy = Purchase.objects.filter(
                            name=app.name, 
                            quantity=app.quantity, 
                            requester=app.owner
                        ).first()
                        if not buy:
                            Purchase.objects.create(
                                name=app.name,
                                quantity=app.quantity,
                                requester=app.owner
                        )
                        buy.save()

                    if prod.quantity == 0:
                        print(f"{prod} reached 0, deleting")
                        prod.delete()
                    else:
                        prod.save()
                    app.delete()
                else:
                    print(f"None were found, creating buy")
                    buy = Purchase.objects.filter(
                            name=app.name, 
                            quantity=app.quantity, 
                            requester=app.owner
                        ).first()
                    if not buy:
                        Purchase.objects.create(
                            name=app.name,
                            quantity=app.quantity,
                            requester=app.owner
                    )
            print(f"{app} resolved, setting from {app.status} to seen")
            app.status = "seen"
            app.save()

    context = {
        "products": Product.objects.filter(),
        "users": User.objects.filter(),
        "applications": Application.objects.filter()
    }
    
    return render(request, 'admin_panel.html', context)
    


@login_required
@verified_check
def change_password(request):
    return render(request, 'change_password.html', {})


def help(request):
    return render(request, 'help.html', {})


@login_required
@verified_check
def inventory(request):
    '''
    ACTIONS = [
        ('drop', 'Списать оборудование'),
        ('request', 'Запросить оборудование')
    ]
    '''
    if request.method == "POST":
        # Получаем от пользователя имя, кол-во нужного Product и action(Удалить, добавить)
        name = request.POST.getlist('name')
        quantity = list(map(int, request.POST.getlist('quantity')))
        action = request.POST.getlist('action')
        state = request.POST.getlist('state')
        print(f"User sent POST to inventory, got: {name, quantity, action, state}")
        try:
            for q in quantity:
                if q <= 0:
                    raise ValueError("Количество должно быть положительным числом.")
        except (ValueError, TypeError):
            messages.error(request, "Некорректное количество! Введите положительное число.")

        # Заявка отправляется в бд. В панели админа отображаются все заявки и одобряются или отклоняются
        for i in range(len(name)):
            existing_app = Application.objects.filter(
                name=name[i], 
                quantity=quantity[i], 
                action=action[i], 
                state=state[i],
                owner=request.user
            ).first()
            if not existing_app:
                Application.objects.create(
                    name=name[i], 
                    quantity=quantity[i], 
                    action=action[i], 
                    state=state[i],
                    owner=request.user
                )
                messages.success(request, "Ваша заявка будет рассмотрена.")
            else:
                ...

        return redirect('inventory')

    # Получаем продукты пользователя
    products = Product.objects.filter(owner=request.user)
    return render(request, 'inventory.html', {'products': products})


def login(request):
    return render(request, 'login.html', {})


def not_verified(request):
    return render(request, 'not_verified.html', {})


@login_required
def profile(request):
    return render(request, 'profile.html', {})


@login_required
@verified_check
@user_passes_test(is_admin)
def purchases(request):
    context = {
        'purchases': Purchase
    }

    return render(request, 'purchases.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@user_passes_test(is_admin)
def usage_report_view(request):
    # Получаем данные отчётов
    user_report = usage_report()
    db_stats = db_report()
    context = {
        'user_report': user_report,
        'db_stats': db_stats,
        'users': User.objects.filter()
    }

    # user_report и db_stats будут доступны в шаблоне как переменные
    return render(request, 'reports.html', context)


@login_required
@user_passes_test(is_admin)
def storage(request):
    if request.method == "POST":
        user = User.objects.filter(id=request.POST.get("username")).first()
        productname = request.POST.get("productname")
        state = request.POST.get("state")
        changingproduct = Product.objects.filter(owner=user, name=productname).first()
        changingproduct.state = state
        changingproduct.save()

    context = {
        'products': Product.objects.filter()
    }

    return render(request, 'storage.html', context)

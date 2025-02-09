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


from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .models import User, Application, Product, Purchase

@login_required
@user_passes_test(is_admin)
def admin_panel(request):
    if request.method == "POST":
        handle_post_request(request)

    context = {
        "products": Product.objects.all(),
        "users": User.objects.all(),
        "applications": Application.objects.all(),
    }
    return render(request, 'admin_panel.html', context)



def handle_post_request(request):
    """Обрабатывает POST-запросы админки."""
    if "verification" in request.POST:
        verify_user(request.POST.get("username"))
    elif "approve" in request.POST:
        process_application(
            int(request.POST.get("ident")), request.POST.get("approve")
        )
    elif "action" in request.POST:
        handle_admin_action(request.POST.get("action"), request.POST.get("name"), request.POST.get("quantity"), request.POST.get("username"),  request.POST.get("state"))

def handle_admin_action(action, name, quantity, username, state):
    owner = User.objects.filter(username=username).first()
    quantity = int(quantity)
    if action == "delete":
        prod = Product.objects.filter(name=name, owner=owner, state=state).first()
        if prod:
            prod.quantity = max(0, prod.quantity - quantity)  # Молимся, что quantity >= 0
            if prod.quantity == 0:
                prod.delete()
            else:
                prod.save()
    
    elif action == "add":
        prod, created = Product.objects.get_or_create(
            name=name, owner=owner, state=state,
            defaults={"quantity": 0}  
        )
        prod.quantity += quantity
        prod.save()
    
        

def verify_user(username):
    """Подтверждает пользователя."""
    user = User.objects.filter(username=username).first()
    if user:
        user.verified = True
        user.save()

def process_application(identificator, action):
    """Обрабатывает заявку (accept/reject)."""
    app = Application.objects.filter(ident=identificator).first()
    if not app:
        return

    if action == "reject":
        app.delete()
        return

    handle_application_acceptance(app)

def handle_application_acceptance(app):
    """Обрабатывает принятие заявки."""
    with transaction.atomic():
        prod = Product.objects.filter(name=app.name, owner=app.owner, state=app.state).first()

        if not prod:
            create_purchase_request(app)
        else:
            modify_existing_product(prod, app)

        app.status = "seen"
        app.save()

def create_purchase_request(app):
    """Создаёт запись о покупке, если товара нет в наличии."""
    purchase, created = Purchase.objects.get_or_create(name=app.name, quantity=app.quantity, requester=app.owner)
    if not created:
        purchase.quantity += app.quantity
        purchase.save()

def modify_existing_product(prod, app):
    """Обновляет данные о продукте или создаёт новый, если требуется."""
    if app.action == "drop":
        if prod.state != "broken":
            Product.objects.create(name=app.name, owner=None, state="broken")
        elif prod.quantity >= app.quantity:
            prod.quantity -= app.quantity
            Product.objects.create(name=app.name, owner=None, quantity=app.quantity, state="inactive")
    elif app.action == "request":
        storage_prod = Product.objects.filter(name=app.name, owner=None).first()
        if storage_prod:
            storage_prod.quantity -= app.quantity
            prod.quantity += app.quantity
        else:
            create_purchase_request(app)

    if prod.quantity == 0:
        prod.delete()
    else:
        prod.save()

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

@login_required
@verified_check
def applications(request):
    applications = Application.objects.filter(owner=request.user)
    return render(request, 'applications.html', {'applications': applications})

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
    if request.method == "POST":
        handle_purchase_action(request.POST.get("verification"), request.POST.get("distributor"), request.POST.get("price"), request.POST.get("ident"))
    DISTRIBUTORS = ["РосСпротНадзор", "СпортЦентр", "СпортБег"]
    context = {
        'purchases': Purchase.objects.filter(),
        'distributors' : DISTRIBUTORS
    }

    return render(request, 'purchases.html', context)

def handle_purchase_action(action, distributor, price, id):
    purchase = Purchase.objects.filter(ident=id).first()
    if action == "reject":
        purchase.delete()
        return
    elif action == "accept":
        prod, created = Product.objects.get_or_create(
            name=purchase.name, owner=None, state=purchase.state, quantity=purchase.quantity,
        )
        prod.quantity += purchase.quantity
        prod.save()
        purchase.distributor = distributor
        purchase.price = price
        purchase.state = "bought"
        purchase.save()
        return

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

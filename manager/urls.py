from telnetlib import LOGOUT

from django.urls import path
from django.shortcuts import redirect
from . import views
from .views import error_404_view
from django.contrib.auth.views import LoginView, LogoutView

# URL-пути
urlpatterns = [
    path('', lambda request: redirect('inventory', permanent=False)),  # Редирект на /login
    path('404/', views.error_404_view, name="404"),
    path('admin_panel/', views.admin_panel, name="admin_panel"),
    path('change_password/', views.change_password, name="change_password"),
    path('help/', views.help, name="help"),
    path('inventory/', views.inventory, name="inventory"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('not_verified/', views.not_verified, name='not_verified'),
    path('profile/', views.profile, name="profile"),
    path('purchases/', views.purchases, name="purchases"),
    path('register/', views.register, name="register"),
    path('reports/', views.usage_report_view, name="reports"),
    path('storage/', views.storage, name="storage")
]

# Указываем кастомный обработчик 404
handler404 = error_404_view

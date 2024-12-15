from django.urls import path
from . import views
from .views import error_404_view
from django.contrib.auth.views import LoginView

# URL-пути
urlpatterns = [
    path('', views.login, name="login"),
    path('help/', views.help, name="help"),
    path('register/', views.register, name="register"),
    path('inventory/', views.inventory, name="inventory"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
]

# Указываем кастомный обработчик 404
handler404 = error_404_view

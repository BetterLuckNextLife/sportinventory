from django.urls import path
from . import views
from .views import error_404_view

# URL-пути
urlpatterns = [
    path('', views.login, name="login"),
    path('help/', views.help, name="help"),
    path('register/', views.register, name="register"),
    path('inventory/', views.inventory, name="inventory"),
]

# Указываем кастомный обработчик 404
handler404 = error_404_view

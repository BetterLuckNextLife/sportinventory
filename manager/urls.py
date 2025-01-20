from django.urls import path
from . import views
from .views import error_404_view
from django.contrib.auth.views import LoginView

# URL-пути
urlpatterns = [
    path('help/', views.help, name="help"),
    path('register/', views.register, name="register"),
    path('inventory/', views.inventory, name="inventory"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('profile/', views.profile, name="profile"),
    path('change_password/', views.change_password, name="change_password"),
    path('404/', views.error_404_view, name="404"),
]

# Указываем кастомный обработчик 404
handler404 = error_404_view
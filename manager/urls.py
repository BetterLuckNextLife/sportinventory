from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('help/', views.help, name="help"),
    path('register/', views.register, name="register"),
    path('user/', views.user, name="user"),
]
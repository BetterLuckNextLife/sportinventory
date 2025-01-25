from django.contrib import admin
from .models import User, Product, Purchase

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Purchase)
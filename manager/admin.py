from django.contrib import admin
from .models import Application, User, Product, Purchase

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Application)

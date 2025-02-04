# Да простят меня вебдевы за то, что я сейчас напишу
from .models import *
from django.db.models import Count, F, Q


def usage_report():
    users = User.objects.annotate(
        active_count=Count('products', filter=Q(products__state='active')),
        inactive_count=Count('products', filter=Q(products__state='inactive')),
        broken_count=Count('products', filter=Q(products__state='active'))
    )
    report = []
    for user in users:
        report.append({
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'active_count': user.active_count,
        })

    return report


def db_report():
    return {'users': User.objects.count(), 'products': Product.objects.count(), 'purchases': Purchase.objects.count()}

# Generated by Django 5.1.5 on 2025-01-28 06:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_remove_application_owner_delete_purchase_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('state', models.CharField(choices=[('none', 'None'), ('bought', 'Куплено'), ('delivered', 'Доставлено')], default='none', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('action', models.CharField(choices=[('None', 'None'), ('drop', 'Списать оборудование'), ('request', 'Запросить оборудование')], default='None', max_length=32)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-08 11:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_alter_product_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='distributor',
            field=models.CharField(choices=[('bought1', 'Куплено1'), ('bought2', 'Куплено2'), ('bought3', 'Куплено3')], default='СпортЦентр', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='price',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='requester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL),
        ),
    ]

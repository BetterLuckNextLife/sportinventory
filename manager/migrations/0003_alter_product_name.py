# Generated by Django 5.1.4 on 2024-12-13 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_rename_state_user_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=256),
        ),
    ]

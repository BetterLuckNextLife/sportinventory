# Generated by Django 5.1.4 on 2024-12-13 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='state',
            new_name='verified',
        ),
    ]
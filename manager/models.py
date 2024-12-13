from django.db import models

# класс для работы с пользователями (учителями)

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    patronymic = models.CharField(max_length=64, blank=True, null=True)
    password_hash = models.CharField(max_length=128)
    verified = models.BooleanField()

    def __str__(self):
        return f"{self.username} ({self.name} {self.surname})"

# класс для работы с вещами(спортивного инвентаря)

class Product(models.Model):
    STATE_CHOICES = [
        ('active', 'Используется'),
        ('inactive', 'В запасе'),
        ('broken', 'Сломан'),
    ]
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='products', blank=True, null=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='inactive')

    def __str__(self):
        return f"{self.name} ({self.get_state_display()})"
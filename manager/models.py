from django.db import models

# класс для работы с пользователями (учителями)

from django.contrib.auth.models import AbstractUser


# Кастомная модель User
class User(AbstractUser):
    # Остальные поля уже есть в AbstractUser
    patronymic = models.CharField(max_length=64, blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


# Класс для спортивного инвентаря
class Product(models.Model):
    STATE_CHOICES = [
        ('active', 'Используется'),
        ('inactive', 'В запасе'),
        ('broken', 'Сломан'),
    ]

    name = models.CharField(max_length=256)
    quantity = models.PositiveIntegerField(default=1)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='inactive')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', blank=True, null=True)

    def __str__(self):
        return f"{self.name} x{self.quantity} ({self.get_state_display()})"


# Пользователь создаёт запрос. После одобрения все изменения вносятся в базу и запись удаляется
class Application(models.Model):
    ident = models.AutoField(primary_key=True)
    ACTIONS = [
        ('drop', 'Списать оборудование'),
        ('request', 'Запросить оборудование')
    ]
    STATE_CHOICES = [
        ('active', 'Используется'),
        ('inactive', 'В запасе'),
        ('broken', 'Сломан'),
    ]
    STATUS =[
        ('seen', 'Рассмотрено'),
        ('unseen', 'Не рассмотрено')
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')  # Автор заявки
    name = models.CharField(max_length=256)
    quantity = models.PositiveIntegerField(default=1)
    state = models.CharField(max_length=8, choices=STATE_CHOICES, default='inactive')
    status = models.CharField(max_length=8, choices=STATUS, default='unseen')
    '''if action == "request":
            ...
    На запрос выделяем quantity вещей. Если у storage нет такого количества, то закупаем через Purchase'''
    action = models.CharField(max_length=32, choices=ACTIONS, default='drop', null=True, blank=True)


class Purchase(models.Model):
    ident = models.AutoField(primary_key=True)
    STATES = [
        ('bought', 'Куплено'),
        ('delivered', 'Доставлено'),
        ('waiting', 'Ожидается')
    ]
    DISTRIBUTORS = [
        ('RosSportNadzor', 'РосСпротНадзор'),
        ('SportCenter', 'СпортЦентр'),
        ('Sportbeg', 'СпортБег'),
    ]
    name = models.CharField(max_length=256)
    quantity = models.PositiveIntegerField(default=1)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')  # Автор заявки
    state = models.CharField(max_length=20, choices=STATES, default='waiting')
    distributor = models.CharField(max_length=20, choices=DISTRIBUTORS)
    price = models.PositiveIntegerField(default=100)
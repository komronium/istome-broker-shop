from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, verbose_name='Электронная почта')
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Полное имя')
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name='Номер телефона')
    inn = models.CharField(max_length=15, null=True, blank=True, verbose_name='ИНН организации')
    is_partner = models.BooleanField(default=False, verbose_name='Партнер?')
    date_joined = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Дата регистрации')

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

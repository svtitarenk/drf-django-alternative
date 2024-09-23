from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта', help_text='Укажите почту')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='телефон', help_text='Укажите телефон')
    tg_nick = models.CharField(max_length=255, **NULLABLE, verbose_name='Tg name', help_text='укажите ник телеграмм')
    avatar = models.ImageField(upload_to='users/avatar/', **NULLABLE, verbose_name='Аватар',
                               help_text='Загрузите аватар')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

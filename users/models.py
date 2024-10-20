from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта', help_text='Укажите почту')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='телефон', help_text='Укажите телефон')
    tg_nick = models.CharField(max_length=255, **NULLABLE, verbose_name='Tg name', help_text='укажите ник телеграмм')
    avatar = models.ImageField(upload_to='users/avatar/', **NULLABLE, verbose_name='Аватар',
                               help_text='Загрузите аватар')
    tg_chat_id = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name='id чата в Телеграмм',
        help_text='Укажите id чата в Телеграмм',
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Donation(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Сумма пожертвования',
        help_text='Укажите сумму пожертвования',
    )
    session_id = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name='id сессии',
        help_text='Укажите id сессии',
    )
    link = models.URLField(
        max_length=400,
        **NULLABLE,
        verbose_name='Ссылка на оплату',
        help_text='Укажите ссылку на оплату',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
        on_delete=models.CASCADE,
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Пожертвование"
        verbose_name_plural = "Пожертвования"

    def __str__(self):
        return f'{self.amount} руб. от {self.user}'


from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

NULLABLE = {
    'null': True,
    'blank': True
}


class UserRoles(models.TextChoices):

    MEMBER = 'member', _('member')
    MODERATOR = 'moderator', _('moderator')


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=30, unique=True, verbose_name='Почта')
    phone = models.CharField(max_length=20, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=20, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='users', verbose_name='Аватар', **NULLABLE)
    role = models.CharField(max_length=9, choices=UserRoles.choices, default=UserRoles.MEMBER)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40, null=True, verbose_name='ФИО')
    email = models.EmailField(max_length=40, null=True, unique=True, verbose_name='Введите вашу почту')
    password = models.CharField(max_length=150, unique=True, verbose_name='Введите пароль')
    otp = models.CharField(max_length=4, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'name']

    objects = UserManager()

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        app_label = 'users'
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователь'


class PasswordResetOtp(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, unique=True)
    time = models.DateTimeField()

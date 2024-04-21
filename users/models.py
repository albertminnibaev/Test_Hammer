from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    password = None

    phone = PhoneNumberField(unique=True, verbose_name="номер телефона")
    first_name = models.CharField(max_length=100, verbose_name='имя пользователя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия пользователя')
    referral_code_refer = models.CharField(max_length=6, **NULLABLE)
    refer = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE)
    otp_code = models.CharField(max_length=4, verbose_name='код доступа')
    referral_code = models.CharField(max_length=6, unique=True, verbose_name='реферральный код пользователя', **NULLABLE)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def check_otp_code(self, otp_code):
        """
        Метод проверяет соответствие кода подтверждения пользовательскому коду подтверждения.
        """
        return self.otp_code == otp_code

    def __str__(self):
        return f'{self.first_name}, {self.last_name} ({self.phone})'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

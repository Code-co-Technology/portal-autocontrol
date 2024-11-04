from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+9989999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=250, null=True, blank=True, verbose_name="Телефон", unique=True)
    avatar = models.ImageField(upload_to='avatar/', null=True, blank=True, verbose_name="Аватар")


    def __str__(self):
        return self.username

    class Meta:
        db_table = "table_user"
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

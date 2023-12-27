from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        if not username:
            raise ValueError('Users must have a username!')
        if not email:
            raise ValueError('Users must have an email!')
        if not password:
            raise ValueError('Users must have a password!')

        return user

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(username=username, email=email, password=password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    date_created = models.DateField(null=False, blank=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

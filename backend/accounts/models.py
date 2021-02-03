from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from rest_framework.response import Response


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            return Response('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=222, unique=True)
    first_name = models.CharField(max_length=222)
    last_name = models.CharField(max_length=222)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def get_full_name(self):
        return self.first_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email
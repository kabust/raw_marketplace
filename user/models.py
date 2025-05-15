from django.contrib.auth.models import (
    BaseUserManager,
)
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

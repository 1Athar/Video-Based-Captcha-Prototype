from django.db import models
from django.contrib.auth.models import make_password,AbstractBaseUser, BaseUserManager
from .managers import UserManager
class RegisteredUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
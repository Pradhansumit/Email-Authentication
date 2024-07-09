from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from api import backend


# CUSTOM USER MODEL
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)
    password = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = backend.UserManager()  # connects to the user manager.

    def __str__(self):
        return self.first_name + " " + self.last_name

    def is_active(self):
        return True

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from api import backend


# CUSTOM USER MODEL
class CustomUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=50)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    objects = backend.UserManager()  # connects to the user manager.

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email

    # def is_active(self):
    #     return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# TOKEN MODEL
class TokenModel(models.Model):
    user = models.EmailField(unique=True)
    token = models.CharField(max_length=200)
    isVerified = models.BooleanField(default=False)

from django.contrib.auth.base_user import BaseUserManager


# MANAGER FOR CUSTOM USER MODEL
class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email and not phone_number:
            raise ValueError("Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, phone_number, password=None):
        if not email and not phone_number:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self.db)

        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        return user

    # def get_by_natural_key(self, username):
    #     return self.get({self.model.USERNAME_FIELD: username})

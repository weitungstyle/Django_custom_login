from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError("Username is required.")
        if not password:
            raise ValueError("Password is required.")
        if username.isspace():
            raise ValueError("Username cannot be empty.")
        if len(username) < 3 or len(username) > 32:
            raise ValueError("Username must be between 3 - 32 characters.")
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def validate_password(self, password):
        """
        Validates that a password meets the complexity requirements.
        """
        if len(password) < 8 or len(password) > 32:
            raise ValueError("Password must be between 8 - 32 characters.")
        if not any(char.isupper() for char in password):
            raise ValueError(
                'Password must contain at least one uppercase letter.')
        if not any(char.islower() for char in password):
            raise ValueError(
                'Password must contain at least one lowercase letter.')
        if not any(char.isdigit() for char in password):
            raise ValueError('Password must contain at least one digit.')
        return True


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=32, unique=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    last_failed_attempt = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'username'
    objects = CustomUserManager()

    def __str__(self):
        return self.username

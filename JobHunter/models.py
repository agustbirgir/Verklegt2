from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None  # Disable the username field
    email = models.EmailField('email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No need for email in REQUIRED_FIELDS since it's the USERNAME_FIELD

    def __str__(self):
        return self.email

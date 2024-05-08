from django.db import models
from django.contrib.auth.models import AbstractUser


class User(models.Model, AbstractUser):
    username = None
    # Automatically creates an ID field for each user
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

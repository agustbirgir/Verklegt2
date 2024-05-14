from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    username = None  # Disable the username field
    email = models.EmailField('email address', unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No need for email in REQUIRED_FIELDS since it's the USERNAME_FIELD

    def is_jobHunter(self):
        return True

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    phone_number = models.CharField(max_length=15, blank=True)
    street_name = models.CharField(max_length=255, blank=True)
    house_number = models.CharField(max_length=10, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.email}'
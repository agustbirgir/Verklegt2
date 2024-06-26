from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from Company.models import Job

class User(AbstractUser):
    username = None
    email = models.EmailField('email address', unique=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
    city = models.CharField(max_length=50, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return f'Profile of {self.user.email}'

class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True, related_name='applications')  # Add related_name here
    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    street_name = models.CharField(max_length=255, null=True, blank=True)
    house_number = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, default='Reykjavik')
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=100, default='Iceland')
    cover_letter = models.TextField()
    status = models.CharField(max_length=20, default='pending')
    applied_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.job.title}'

class Experience(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='experiences')
    place_of_work = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.place_of_work} - {self.role}'

class Recommendation(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='recommendations')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    can_contact = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.role}'

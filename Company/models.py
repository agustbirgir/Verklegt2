from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CompanyManager(BaseUserManager):
    print("Starting to load Company models")

    def create_company(self, email, password, company_name, address, about_company, company_image=None, cover_image=None):
        if not email:
            raise ValueError("Companies must have an email address")
        email = self.normalize_email(email)
        company = self.model(
            email=email,
            company_name=company_name,
            address=address,
            about_company=about_company,
            company_image=company_image,
            cover_image=cover_image
        )
        company.set_password(password)
        company.save(using=self._db)
        return company

class Company(AbstractBaseUser):
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    about_company = models.TextField(null=True, blank=True)
    company_image = models.ImageField(upload_to='company_images/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    last_login = models.DateTimeField(default=timezone.now, verbose_name='last login')

    objects = CompanyManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name']

    def isCompany(self):
        return True

    def __str__(self):
        return self.company_name

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="jobs")
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    expiration_date = models.DateField()
    job_type = models.CharField(max_length=20)  # Full Time or Part Time
    categories = models.TextField()  # Could be serialized list of categories or many-to-many field

    def __str__(self):
        return self.job_title
    print("finished loading company models")
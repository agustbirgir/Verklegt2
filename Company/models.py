from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class CompanyManager(BaseUserManager):
    def create_company(self, email, password, company_name, address, about_company, postal_code=None, city=None, company_image=None, cover_image=None):
        if not email:
            raise ValueError("Companies must have an email address")
        email = self.normalize_email(email)
        company = self.model(
            email=email,
            company_name=company_name,
            address=address,
            about_company=about_company,
            postal_code=postal_code,
            city=city,
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
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    company_image = models.ImageField(upload_to='company_images/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='cover_images/', null=True, blank=True)
    last_login = models.DateTimeField(default=timezone.now, verbose_name='last login')

    objects = CompanyManager()  # Ensure the custom manager is used

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name']

    def is_company(self):
        return True

    def __str__(self):
        return self.company_name

class JobCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    exp_date = models.DateField()
    job_type = models.CharField(max_length=50, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time')])
    categories = models.ManyToManyField(JobCategory)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_job'

    def __str__(self):
        return self.title

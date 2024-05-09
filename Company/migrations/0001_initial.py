# Generated by Django 4.0.4 on 2024-05-09 15:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('company_name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True, null=True)),
                ('about_company', models.TextField(blank=True, null=True)),
                ('company_image', models.ImageField(blank=True, null=True, upload_to='company_images/')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='cover_images/')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

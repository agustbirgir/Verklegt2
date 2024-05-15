from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0003_alter_job_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('exp_date', models.DateField()),
                ('job_type', models.CharField(max_length=50, choices=[('Full Time', 'Full Time'), ('Part Time', 'Part Time')])),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Company.company')),
            ],
            options={
                'db_table': 'company_job',
            },
        ),
        migrations.CreateModel(
            name='JobCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='categories',
            field=models.ManyToManyField(to='Company.JobCategory'),
        ),
    ]

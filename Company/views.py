from django.shortcuts import render, redirect, get_object_or_404
from .models import Company, Job, JobCategory
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt


@login_required
def index(request):
    company = request.user
    jobs = Job.objects.all()
    return render(request, 'Company/company_page.html', {'company': company,  'jobs': jobs})

def company_page(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    return render(request, 'Company/company_page.html', {'company': company})

def company_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            print(f"User id: {user.id} logged in")
            login(request, user)
            return redirect('company_index')  # Redirect to a dashboard or appropriate page
        else:
            return render(request, 'Base/comp_login.html', {'error': 'Invalid login credentials'})
    return render(request, 'Base/comp_login.html')


def company_signup(request):
    if request.method == "POST":
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        about_company = request.POST.get('about_company')
        company_image = request.FILES.get('company_image')
        cover_image = request.FILES.get('cover_image')

        if Company.objects.filter(email=email).exists():
            return render(request, 'Company/sign_up.html', {'error': 'Email already in use'})

        new_company = Company.objects.create_company(
            email=email,
            password=password,
            company_name=company_name,
            address=address,
            about_company=about_company,
            company_image=company_image,
            cover_image=cover_image
        )

        print("new company created: ", new_company)
        return redirect('login')

    else:
        return render(request, 'Company/sign_up.html')


@csrf_exempt
@login_required
def new_job(request):
    if request.method == 'POST':
        title = request.POST.get('jobTitle')
        description = request.POST.get('jobDescription')
        address = request.POST.get('address')
        city = request.POST.get('city')
        exp_date = request.POST.get('expDate')
        job_type = request.POST.get('jobType', 'Part Time')
        categories_ids = request.POST.getlist('categories')  # Get the categories from the form
        categories = JobCategory.objects.filter(id__in=categories_ids)  # Get the category objects from the database

        job = Job(
            company=request.user,
            title=title,
            description=description,
            address=address,
            city=city,
            exp_date=exp_date,
            job_type=job_type
        )
        job.save()
        job.categories.set(categories)  # Save the categories to the job

        return redirect('index')

    else:
        categories = JobCategory.objects.all()
        return render(request, 'Company/new_job.html', {'categories': categories})
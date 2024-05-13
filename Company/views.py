from django.shortcuts import render, redirect
from .models import Company, Job
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
import json


def index(request):
    return render(request, 'Company/index.html')


def company_page(request):
    return render(request, 'Company/company_page.html')


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


@login_required
def new_job(request):
    if request.method == 'POST':
        print("user authenticated: ", request.user.is_authenticated)
        job_title = request.POST.get('jobTitle')
        job_description = request.POST.get('jobDescription')
        address = request.POST.get('address')
        city = request.POST.get('city')
        expiration_date = request.POST.get('expDate')
        job_type = request.POST.get('jobType', 'Part Time')  # Adjusted to use correct name
        categories = request.POST.getlist('categories')  # Adjusted to handle list of categories

        # Ensure categories are serialized to JSON format properly
        categories_json = json.dumps(categories, cls=DjangoJSONEncoder)

        job = Job(
            company=request.user,  # Directly use request.user here since it is the Company instance
            job_title=job_title,
            job_description=job_description,
            address=address,
            city=city,
            expiration_date=expiration_date,
            job_type=job_type,
            categories=categories_json  # Ensure this is properly formatted JSON
        )
        job.save()

        return redirect('index')  # Redirect to a success page after saving

    return render(request, 'Company/new_job.html')

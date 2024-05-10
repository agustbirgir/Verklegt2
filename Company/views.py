from django.shortcuts import render, redirect
from .models import Company
from django.contrib.auth.hashers import make_password


def index(request):
    return render(request, 'Company/index.html')

def company_page(request):
    return render(request, 'Company/company_page.html')

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

def new_job(request):
    if request.method == 'POST':
        pass
    return render(request, 'Company/new_job.html')


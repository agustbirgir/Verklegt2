from django.shortcuts import render, redirect
from .models import User, Profile # Jobhunter model
from Company.models import Company,CompanyManager
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.cache import never_cache


@never_cache
def index(request):
    return render(request, 'JobHunter/index.html')

def card(request):
    return render(request, 'Base/card.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # First, try to authenticate normally
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            if hasattr(user, 'company_name'):
                print("User is a company. Redirecting to company index.")
                return redirect('company_index')
            else:
                print("User is a jobhunter. Redirecting to jobhunter index.")
                return redirect('index')
        else:
            # If no user is found, check if it might be a Company
            try:
                company_user = Company.objects.get(email=email)
                if company_user.check_password(password):
                    login(request, company_user)
                    print("Logged in Company user manually.")
                    return redirect('company_index')
                else:
                    print("Password check failed for Company.")
            except Company.DoesNotExist:
                print("No company found with that email.")

            return HttpResponse("Invalid login credentials", status=401)

    return render(request, 'Base/login.html')

def logout_view(request):
    print("logging out: ", request.user)
    logout(request)
    print("User after logout",request.user)
    return redirect('login')

def signup_choice(request):
    return render(request, 'Base/choose_signup.html')

def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email=email).exists():
            print("Email already in use: ", email)
            return render(request, 'JobHunter/sign_up.html', {'error': 'Email already in use'})

        if password == confirm_password:
            hashed_password = make_password(password)
            # Creating user
            new_user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=hashed_password
            )
            # Creating profile linked to the user
            Profile.objects.create(user=new_user)
            print("new user created: ", new_user)
            return redirect('login')
        else:
            print("password mismatch ", email)
            return render(request, 'JobHunter/sign_up.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'JobHunter/sign_up.html')

def job_description_view(request):
    return render(request, 'Base/job_description.html')

def user_profile_view(request):
    return render(request, 'Base/user_profile.html')
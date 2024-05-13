from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile#, Job_Application # Jobhunter model
from Company.models import Company, CompanyManager, Job
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.cache import never_cache


@never_cache
def index(request):
    jobs = Job.objects.all()
    return render(request, 'JobHunter/index.html', {'jobs': jobs})


def card(request):
    jobs = Job.objects.all()  # Retrieve all jobs from your database
    return render(request, 'Base/card.html', {'jobs': jobs})

@login_required
def user_profile_view(request):
    # Assuming the user is logged in, get their profile
    user_profile = get_object_or_404(Profile, user=request.user)

    # Create a context dictionary to pass to the template
    context = {
        'user': request.user,
        'bio': user_profile.bio,
        # Additional data can be included here if needed
    }

    # Pass the context to the template
    return render(request, 'JobHunter/user_profile.html', context)

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
                    print(f"Logged in Company user manually. Company ID: {company_user.id}")
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
        bio = request.POST.get('bio', '').strip()  # Ensure this is captured

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
            Profile.objects.create(user=new_user, bio=bio)
            print("new user created: ", new_user)
            return redirect('login')
        else:
            print("password mismatch ", email)
            return render(request, 'JobHunter/sign_up.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'JobHunter/sign_up.html')

def job_description_view(request):
    return render(request, 'Base/job_description.html')


@login_required
def user_profile_view(request):
    # Retrieve the user's profile and check for applied jobs
    user_profile = get_object_or_404(Profile, user=request.user)
    #applied_jobs = JobApplication.objects.filter(user=request.user)  # Assuming there's a JobApplication model

    context = {
        'user': request.user,
        'bio': user_profile.bio,
        'email': request.user.email,
        #'applied_jobs': applied_jobs,
        # 'profile_image': user_profile.image.url if user_profile.image else 'path/to/default/image.jpg'
    }

    return render(request, 'JobHunter/user_profile.html', context)


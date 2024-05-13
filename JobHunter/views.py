from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile#, Job_Application # Jobhunter model
from Company.models import Company, CompanyManager
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from .forms import EditProfileForm


@never_cache
def index(request):
    return render(request, 'JobHunter/index.html')


def card(request):
    return render(request, 'Base/card.html')

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
    # Retrieve the user's profile
    user_profile = get_object_or_404(Profile, user=request.user)

    # Create a context dictionary to pass to the template
    context = {
        'user': request.user,
        'bio': user_profile.bio,
        'profile_image': user_profile.profile_image.url if user_profile.profile_image else None,
        'phone_number': user_profile.phone_number,
        'street_name': user_profile.street_name,
        'house_number': user_profile.house_number,
        'postal_code': user_profile.postal_code,
        'country': user_profile.country,
        # Additional data can be included here if needed
    }

    # Pass the context to the template
    return render(request, 'JobHunter/user_profile.html', context)

@login_required
def profile_edit_view(request):
    # Retrieve the user's profile
    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        # If the form has been submitted, update the user's profile

        # Create a form instance with the POST data
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            # If the form is valid, save the changes and redirect to the user's profile page
            form.save()
            return redirect('user_profile')

    else:
        # If the form has not been submitted, display the form with the user's current profile information
        form = ProfileForm(instance=user_profile)

    # Create a context dictionary to pass to the template
    context = {
        'form': form,
    }

    # Pass the context to the template
    return render(request, 'JobHunter/profile_edit.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'JobHunter/profile_edit.html', {'form': form})
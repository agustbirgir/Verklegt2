from django.shortcuts import render, redirect
from .models import User, Profile
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
        if request.user.is_authenticated:
            return redirect('index')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Invalid login", status=401)
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
    return render(request, 'JobHunter/user_profile.html')


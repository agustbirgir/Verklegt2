from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.http import HttpResponse



def index(request):
    return render(request, 'JobHunter/index.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print("email is: ", email)
        password = request.POST.get('password')
        print("password is: ", password)
        # Debugging prints
        print("Debug: Email received:", email)
        print("Debug: Password received:", password)
        if request.user.is_authenticated:
            return redirect('index')
        else:
            print("Login failed")
            user = authenticate(email=email, password=password)

        # Authenticate the user
        print("Login worked")
        user = authenticate(request, email=email, password=password)  # Assuming username is the email
        if user is not None:
            print("Debug: Authentication successful for user:", user.email)
            login(request, user)
            return redirect('index')
        else:
            print("Debug: Authentication failed for email:", email)
            return HttpResponse("Invalid login", status=401)
    else:
        return render(request, 'Base/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            print("Email already in use: ", email)
            return render(request, 'JobHunter/sign_up.html', {'error': 'Email already in use'})

        if password == confirm_password:
            hashed_password = make_password(password)
            new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            print("new user created: ", new_user)
            return redirect('login')
        else:
            print("password mismatch ", email)
            return render(request, 'JobHunter/sign_up.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'JobHunter/sign_up.html')

def job_description_view(request):
    return render(request, 'Base/job_description.html')
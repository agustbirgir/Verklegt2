from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'JobHunter/index.html')

def login_view(request):
    return render(request, 'Base/login.html')

def signup_view(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            first_name, last_name = full_name.split()
            hashed_password = make_password(password)
            User.objects.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
            return redirect('login')
        else:
            return render(request, 'JobHunter/sign_up.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'JobHunter/sign_up.html')
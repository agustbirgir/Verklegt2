from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'JobHunter/index.html')

def login_view(request):
    return render(request, 'JobHunter/login.html')

def signup_view(request):  # Add this function
    return render(request, 'JobHunter/sign_in.html')
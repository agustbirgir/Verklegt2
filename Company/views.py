from django.shortcuts import render, redirect
# Create your views here.

def index(request):
    return render(request, 'Company/index.html')

def company_signup(request):
    if request.method == 'POST':
        pass
    return render(request, 'Company/sign_up.html')

def new_job(request):
    if request.method == 'POST':
        pass
    return render(request, 'Company/new_job.html')
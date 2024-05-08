from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request, 'Company/index.html')

def company_signup(request):
    if request.method == 'POST':
        pass
    return render(request, 'Company/sign_up.html')
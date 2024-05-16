from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Profile, Application, Experience, Recommendation
from Company.models import Company, Job, JobCategory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from .forms import EditProfileForm
from django.utils import timezone
from django.db.models import Q
import logging
from django.shortcuts import render


User = get_user_model()

def index(request):
    query = request.GET.get('q')
    category_filter = request.GET.getlist('category')

    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(company__company_name__icontains=query))

    if category_filter:
        jobs = jobs.filter(categories__id__in=category_filter).distinct()

    categories = JobCategory.objects.all()

    return render(request, 'JobHunter/index.html', {'jobs': jobs, 'categories': categories, 'query': query, 'category_filter': category_filter})




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
            try:
                # Check if the user is associated with a company
                company_user = Company.objects.get(email=email)
                print(f"User is a company. Redirecting to company index. with id: {company_user.id}")  # id here
                return redirect('company_index')
            except Company.DoesNotExist:
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
        bio = request.POST.get('bio', '').strip()

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

def job_description_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    print(f"Job: {job}")  # Debugging: Check the job object
    print(f"Company ID: {job.company.id}")  # Debugging: Check the company id
    print(f"Categories: {[category.name for category in job.categories.all()]}")  # Debugging: Check the job's categories
    return render(request, 'Base/job_description.html', {'job': job})

@login_required
def user_profile_view(request):
    # Retrieve the user's profile and check for applied jobs
    user_profile = get_object_or_404(Profile, user=request.user)
    #applied_jobs = JobApplication.objects.filter(user=request.user)  # Assuming there's a JobApplication model

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
            print(form.cleaned_data)  # Add this line
            form.save()
            return redirect('user_profile')
        else:
            print(form.errors)

    else:
        # If the form has not been submitted, display the form with the user's current profile information
        form = ProfileForm(instance=user_profile)

    # Create a context dictionary to pass to the template
    context = {
        'form': form,
    }

    # Pass the context to the template
    return render(request, 'JobHunter/profile_edit.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=request.user.profile)
    return render(request, 'JobHunter/profile_edit.html', {'form': form})


@login_required
def application_view(request, job_id):
    job = get_object_or_404(Job, id=job_id)  # Ensure the job exists
    if request.method == 'POST':
        form_data = {
            'job_id': job_id,
            'full_name': request.POST.get('fullName'),
            'email': request.POST.get('email'),
            'street_name': request.POST.get('streetName'),
            'house_number': request.POST.get('houseNr'),
            'city': request.POST.get('city'),
            'postal_code': request.POST.get('postalCode'),
            'country': request.POST.get('country'),
            'cover_letter': request.POST.get('coverLetter'),
            'places_of_work': request.POST.getlist('placeOfWork[]'),
            'roles': request.POST.getlist('role[]'),
            'start_dates': request.POST.getlist('startDate[]'),
            'end_dates': request.POST.getlist('endDate[]'),
            'rec_names': request.POST.getlist('rec_name[]'),
            'rec_roles': request.POST.getlist('rec_role[]'),
            'rec_emails': request.POST.getlist('rec_email[]'),
            'rec_phone_numbers': request.POST.getlist('rec_phone_number[]'),
            'rec_can_contacts': request.POST.getlist('rec_can_contact[]')
        }
        request.session['form_data'] = form_data
        return redirect('review_page')

    context = {
        'job': job,
        'company_name': job.company.company_name,
        'title': job.title
    }
    return render(request, 'JobHunter/application.html', context)

logger = logging.getLogger(__name__)
@login_required
def review_page(request):
    form_data = request.session.get('form_data', None)
    if not form_data:
        return redirect('index')  # Redirect to index if no form data is found

    job_id = form_data.get('job_id')
    job = get_object_or_404(Job, id=job_id)

    has_cover = bool(form_data.get('cover_letter'))
    has_experience = bool(form_data.get('places_of_work')) and any(form_data.get('places_of_work'))
    has_recommendations = bool(form_data.get('rec_names')) and any(form_data.get('rec_names'))

    if request.method == 'POST':
        try:
            # Create and save the application
            application = Application(
                user=request.user,
                job=job,
                full_name=form_data.get('full_name'),
                email=form_data.get('email'),
                street_name=form_data.get('street_name'),
                house_number=form_data.get('house_number'),
                city=form_data.get('city'),
                postal_code=form_data.get('postal_code'),
                country=form_data.get('country'),
                cover_letter=form_data.get('cover_letter'),
                status='pending',
                applied_on=timezone.now()
            )
            application.save()
            logger.debug("Application saved: %s", application)

            # Save experiences
            for i in range(len(form_data['places_of_work'])):
                experience = Experience(
                    application=application,
                    place_of_work=form_data['places_of_work'][i],
                    role=form_data['roles'][i],
                    start_date=form_data['start_dates'][i],
                    end_date=form_data['end_dates'][i]
                )
                experience.save()
                logger.debug("Experience saved: %s", experience)

            # Save recommendations
            for i in range(len(form_data['rec_names'])):
                recommendation = Recommendation(
                    application=application,
                    name=form_data['rec_names'][i],
                    role=form_data['rec_roles'][i],
                    email=form_data['rec_emails'][i],
                    phone_number=form_data['rec_phone_numbers'][i] if i < len(form_data['rec_phone_numbers']) else "",
                    can_contact=(form_data['rec_can_contacts'][i] == 'true') if i < len(form_data['rec_can_contacts']) else False
                )
                recommendation.save()
                logger.debug("Recommendation saved: %s", recommendation)

            request.session.pop('form_data', None)
            return redirect('index')  # Redirect to index after final submission

        except Exception as e:
            logger.error("Error saving application: %s", e)
            # Handle the error appropriately, e.g., show an error message to the user

    context = {
        'company_name': job.company.company_name,
        'title': job.title,
        'full_name': form_data.get('full_name'),
        'email': form_data.get('email'),
        'street_name': form_data.get('street_name'),
        'house_number': form_data.get('house_number'),
        'city': form_data.get('city'),
        'postal_code': form_data.get('postal_code'),
        'country': form_data.get('country'),
        'cover_letter': form_data.get('cover_letter'),
        'has_cover': has_cover,
        'has_experience': has_experience,
        'has_recommendations': has_recommendations,
    }
    return render(request, 'JobHunter/review_page.html', context)


def search(request):
    query = request.GET.get('search', '')
    if query:
        jobs = Job.objects.filter(
            Q(company__company_name__icontains=query) |
            Q(job_title__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    return render(request, 'JobHunter/index.html', {'jobs': jobs, 'query': query})
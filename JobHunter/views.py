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
import pycountry

User = get_user_model()

def index(request):
    jobs = Job.objects.all()
    categories = JobCategory.objects.all()
    companies = Company.objects.all()

    query = request.GET.get('q', '')
    category_filter = request.GET.getlist('category')
    company_filter = request.GET.getlist('company')
    job_type_filter = request.GET.getlist('job_type')
    sort_filter = request.GET.get('sort')

    if query:
        jobs = jobs.filter(
            Q(company__company_name__icontains=query) |
            Q(title__icontains=query)
        )

    if category_filter:
        jobs = jobs.filter(categories__id__in=category_filter)

    if company_filter:
        jobs = jobs.filter(company__id__in=company_filter)

    if job_type_filter:
        jobs = jobs.filter(job_type__in=job_type_filter)

    if sort_filter:
        if sort_filter == 'newest':
            jobs = jobs.order_by('-exp_date')
        elif sort_filter == 'oldest':
            jobs = jobs.order_by('exp_date')

    context = {
        'jobs': jobs,
        'categories': categories,
        'companies': companies,
        'query': query,
        'category_filter': category_filter,
        'company_filter': company_filter,
        'job_type_filter': job_type_filter,
        'sort_filter': sort_filter,
    }

    return render(request, 'JobHunter/index.html', context)

# Function to generate country list
def get_country_list():
    countries = list(pycountry.countries)
    return [country.name for country in countries]


def card(request):
    jobs = Job.objects.all()  # Retrieve all jobs from your database
    return render(request, 'Base/card.html', {'jobs': jobs})

@login_required
def user_profile_view(request):
    user_profile = get_object_or_404(Profile, user=request.user)

    context = {
        'user': request.user,
        'bio': user_profile.bio,
    }

    return render(request, 'JobHunter/user_profile.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            try:
                # Check if the user is associated with a company
                company_user = Company.objects.get(email=email)
                print(f"User is a company. Redirecting to company page with id: {company_user.id}")  # id here
                return redirect('company_page', company_id=company_user.id)
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
                    return redirect('company_page', company_id=company_user.id)
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
    return render(request, 'Base/job_description.html', {'job': job})

@login_required
def user_profile_view(request):
    # Retrieve the user's profile and check for applied jobs
    user_profile = get_object_or_404(Profile, user=request.user)
    applications = Application.objects.filter(user=request.user).select_related('job')

    applications_with_status = []
    status_color_map = {
        'pending': 'orange',
        'accepted': 'green',
        'rejected': 'red',
    }

    for application in applications:
        status_color = status_color_map.get(application.status, 'black')  # Default to black if status is unrecognized
        applications_with_status.append({
            'job': application.job,
            'status': application.status,
            'status_color': status_color,
        })

    context = {
        'user': request.user,
        'bio': user_profile.bio,
        'profile_image': user_profile.profile_image.url if user_profile.profile_image else None,
        'phone_number': user_profile.phone_number,
        'street_name': user_profile.street_name,
        'house_number': user_profile.house_number,
        'postal_code': user_profile.postal_code,
        'country': user_profile.country,
        'applications': applications_with_status,
    }

    return render(request, 'JobHunter/user_profile.html', context)


@login_required
def profile_edit_view(request):

    country_list = get_country_list()
    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':

        form = ProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            print(form.cleaned_data)  # Add this line
            form.save()
            return redirect('user_profile')
        else:
            print(form.errors)

    else:
        form = ProfileForm(instance=user_profile)

    context = {
        'form': form,
        'country_list': country_list,
    }

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
    user = get_object_or_404(User, email=request.user.email)
    profile = get_object_or_404(Profile, user_id=user.id)

    country_list = get_country_list()
    if request.method == 'POST':
        form_data = {
            'job_id': job_id,
            'user_id': profile.id,
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

        # Save the application
        application = Application(
            user=user,
            job=job,
            full_name=form_data['full_name'],
            email=form_data['email'],
            street_name=form_data['street_name'],
            house_number=form_data['house_number'],
            city=form_data['city'],
            postal_code=form_data['postal_code'],
            country=form_data['country'],
            cover_letter=form_data['cover_letter'],
            status='pending',
            applied_on=timezone.now()
        )
        application.save()

        # Save experiences
        for i in range(len(form_data['places_of_work'])):
            Experience.objects.create(
                application=application,
                place_of_work=form_data['places_of_work'][i],
                role=form_data['roles'][i],
                start_date=form_data['start_dates'][i],
                end_date=form_data['end_dates'][i]
            )

        # Save recommendations
        for i in range(len(form_data['rec_names'])):
            Recommendation.objects.create(
                application=application,
                name=form_data['rec_names'][i],
                role=form_data['rec_roles'][i],
                email=form_data['rec_emails'][i],
                phone_number=form_data['rec_phone_numbers'][i] if i < len(form_data['rec_phone_numbers']) else "",
                can_contact=(form_data['rec_can_contacts'][i] == 'true') if i < len(
                    form_data['rec_can_contacts']) else False
            )

        return redirect('review_page', applicant_id=application.id)

    context = {
        'job': job,
        'company_name': job.company.company_name,
        'title': job.title,
        'user': user,
        'profile': profile,
        'country_list': country_list
    }
    return render(request, 'JobHunter/application.html', context)


logger = logging.getLogger(__name__)

@login_required
def review_page(request, applicant_id):
    applicant = get_object_or_404(Application, id=applicant_id)
    job = applicant.job

    is_company = isinstance(request.user, Company)

    if request.method == 'POST':
        try:
            for experience in applicant.experiences.all():
                experience.save()
                logger.debug("Experience saved: %s", experience)

            # Save recommendations
            for recommendation in applicant.recommendations.all():
                recommendation.save()
                logger.debug("Recommendation saved: %s", recommendation)

            return redirect('index')

        except Exception as e:
            logger.error("Error saving application: %s", e)

    context = {
        'applicant': applicant,
        'is_company': is_company,
        'company_name': job.company.company_name,
        'title': job.title,
        'full_name': applicant.full_name,
        'email': applicant.email,
        'street_name': applicant.street_name,
        'house_number': applicant.house_number,
        'city': applicant.city,
        'postal_code': applicant.postal_code,
        'country': applicant.country,
        'cover_letter': applicant.cover_letter,
        'has_cover': applicant.cover_letter is not None,
        'has_experience': applicant.experiences.exists(),
        'has_recommendations': applicant.recommendations.exists(),
    }
    return render(request, 'JobHunter/review_page.html', context)



def search(request):
    query = request.GET.get('q', '')
    jobs = Job.objects.none()
    if query:
        jobs = Job.objects.filter(
            Q(company__company_name__icontains=query) |
            Q(title__icontains=query)
        )
    categories = JobCategory.objects.all()
    companies = Company.objects.all()

    context = {
        'jobs': jobs,
        'query': query,
        'categories': categories,
        'companies': companies,
    }
    return render(request, 'JobHunter/index.html', context)
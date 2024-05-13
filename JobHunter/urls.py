from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('signup_choice/', views.signup_choice, name='signup_choice'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('job_description/', views.job_description_view, name='job_description'),
    path('JobHunter/user_profile/', views.user_profile_view, name='user_profile'),
    path('card/', views.card, name='card'),
    path('application/', views.application_view, name='application'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
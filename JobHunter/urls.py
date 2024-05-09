from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name='login'),
    path('signup_choice/', views.signup_choice, name='signup_choice'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('job_description/', views.job_description_view, name='job_description'),
    path('JobHunter/user_profile/', views.user_profile_view, name='user_profile'),
    path('cards/', views.cards, name='cards'),
]
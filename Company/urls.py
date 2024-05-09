from django.urls import path
from . import  views

"""register the new urls here"""
urlpatterns = [
    path('', views.index, name="index"),
    path('sign_up/', views.company_signup, name="company_signup"),
]
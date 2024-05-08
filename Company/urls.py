from django.urls import path
from . import  views

"""register the new urls here"""
urlpatterns = [
    path('', views.index, name="index"),
    path('', views.index, name="index"),
]
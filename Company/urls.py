from django.urls import path
from . import  views
from django.conf import settings
from django.conf.urls.static import static
"""register the new urls here"""
urlpatterns = [
    path('', views.index, name="index"),
    path('sign_up/', views.company_signup, name="company_signup"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
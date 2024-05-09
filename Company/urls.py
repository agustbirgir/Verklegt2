from django.urls import path
from . import  views
from django.conf import settings
from django.conf.urls.static import static
"""register the new urls here"""
urlpatterns = [
    path('', views.index, name="index"),
    path('sign_up/', views.company_signup, name="company_signup"),
    path('new_job/', views.new_job, name="new_job"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


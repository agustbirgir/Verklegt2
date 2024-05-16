from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="company_index"),
    path('sign_up/', views.company_signup, name="company_signup"),
    path('new_job/', views.new_job, name="new_job"),
    path('company_page/<int:company_id>/', views.company_page, name="company_page"),
    path('login/', views.company_login, name="company_login"),
    path('applicants/<int:job_id>/', views.view_applicants, name="applicants"),
    path('update_status/', views.update_status, name="update_status"),  # New URL pattern
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
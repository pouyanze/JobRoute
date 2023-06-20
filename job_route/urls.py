"""
URL configuration for job_route project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_transfer.views import education_requirements_view, job_transfer_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', job_transfer_view, name='job_transfer'),
    path('job-transfer/', job_transfer_view, name='job_transfer'),
    path('course-suggester/', education_requirements_view, name='course_suggester'),

]

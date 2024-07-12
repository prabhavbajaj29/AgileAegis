# django_project/urls.py

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('issues/', include('issues.urls')),  # Make sure 'issues.urls' is included
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('pricing/', views.pricing, name='pricing'),
    # Other paths as per your application
]

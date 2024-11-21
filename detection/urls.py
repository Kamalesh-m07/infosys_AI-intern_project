from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('register/', views.register_view, name='register'),  # Registration page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),  # Logout functionality
    path('upload-image/', views.upload_media_view, name='upload_image'),  # Image upload page
 # Result page for number plate detection
    path('contact/', views.contact_view, name='contact'),  # Contact page
    path('services/', views.services_view, name='services'),  # Services page
]

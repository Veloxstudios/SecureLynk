from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
     path('services', views.services, name='services'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tools/', views.tools, name='tools'),
    path('tools/portscan/', views.port_scan, name='port_scan'),
    path('profile/', views.profile, name='profile'),
]
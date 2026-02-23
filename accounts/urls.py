from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Auth
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Profile & Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'), 
    path('complete-profile/', views.complete_profile, name='complete_profile'),
    path('msaada/', views.msaada_view, name='msaada_elimu'),
    # Management
    path('members/', views.members_list, name='members_list'),
]

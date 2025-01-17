from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import forms

urlpatterns = [

    path('register/',
        views.register, 
        name='register'),

    path('', 
        auth_views.LoginView.as_view(
        template_name='login.html',
        authentication_form=views.LoginForm
    ), name='login'),

    path('logout/', 
        auth_views.LogoutView.as_view(), 
        name='logout'),

    path('password-reset/', 
        auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        form_class= forms.CustomPasswordResetForm
    ), name='password_reset'),

    path('complete-profile/', 
        views.complete_profile,
        name='complete_profile'),

    path('redirect_profile/', 
         views.redirect_profile, 
         name='redirect_profile'),
]

# Settings à ajouter dans settings.py
LOGIN_REDIRECT_URL = 'complete_profile'
LOGOUT_REDIRECT_URL = 'login'
AUTH_USER_MODEL = 'account.User'
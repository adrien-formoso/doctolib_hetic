# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse_lazy
from .forms import (
    CustomUserCreationForm, 
    LoginForm, 
    MedecinProfileForm,
    PatientProfileForm
)
from .models import User, Patient, Medecin

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Création du profil selon le rôle
            if user.role == User.MEDECIN:
                Medecin.objects.create(
                    user=user,
                    numero_rpps='',  # À compléter plus tard

                )
            else:
                Patient.objects.create(
                    user=user,
                    numero_secu=''  
                )
                
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('complete_profile')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def complete_profile(request):
    user = request.user
    profile = None
    
    # Récupération ou création du profil
    if user.role == User.MEDECIN:
        profile = get_object_or_404(Medecin, user=user)
    else:
        profile = get_object_or_404(Patient, user=user)
    
    if request.method == 'POST':
        if user.role == User.MEDECIN:
            form = MedecinProfileForm(request.POST, instance=profile)
        else:
            form = PatientProfileForm(request.POST, instance=profile)
            
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été complété avec succès!')
            return redirect('profile')
    else:
        if user.role == User.MEDECIN:
            form = MedecinProfileForm(instance=profile)
        else:
            form = PatientProfileForm(instance=profile)
            
    return render(request, 'profiles/complete_profile.html', {
        'form': form,
        'profile': profile
    })

@login_required
def profile(request):
    """Vue pour afficher le profil de l'utilisateur"""
    user = request.user
    if user.role == User.MEDECIN:
        profile = get_object_or_404(Medecin, user=user)
    else:
        profile = get_object_or_404(Patient, user=user)
        
    return render(request, 'profiles/profile.html', {
        'profile': profile
    })
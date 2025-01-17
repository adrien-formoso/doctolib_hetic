from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login , authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
            # Créer l'utilisateur sans le sauvegarder immédiatement
            user = form.save(commit=False)
            
            # Définir le username comme l'email
            user.username = form.cleaned_data['email']
            
            # Sauvegarder l'utilisateur
            user.save()
            
            # Création du profil selon le rôle
            if user.role == User.MEDECIN:
                Medecin.objects.create(
                    user=user,
                    numero_rpps='',  # Sera complété dans complete_profile
                    adresse='',
                    ville='',
                    code_postal='',
                    presentation='',
                )
            else:
                Patient.objects.create(
                    user=user,
                    numero_secu=''  # Sera complété dans complete_profile
                )
                
            # Connecter l'utilisateur
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès! Veuillez compléter votre profil.')
            return redirect('complete_profile')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'register.html', {'form': form})

@login_required
def complete_profile(request):
    user = request.user
    
    # Vérifier si le profil est déjà complet
    if user.role == User.MEDECIN:
        profile = get_object_or_404(Medecin, user=user)
        if profile.numero_rpps:  # Si le profil est déjà complet
            login(request, user)
            return redirect("doctor:doctor_dashboard")
    else:
        profile = get_object_or_404(Patient, user=user)
        if profile.numero_secu:  # Si le profil est déjà complet
            login(request, user)
            return redirect("patient:patient_dashboard")
    
    if request.method == 'POST':
        if user.role == User.MEDECIN:
            form = MedecinProfileForm(request.POST, instance=profile)
        else:
            form = PatientProfileForm(request.POST, instance=profile)
            
        if form.is_valid():
            profile = form.save(commit=False)
            
            # Validation spécifique pour médecin
            if user.role == User.MEDECIN:
                if len(profile.numero_rpps) != 11:
                    messages.error(request, 'Le numéro RPPS doit contenir 11 chiffres.')
                    return render(request, 'complete_profile.html', {'form': form})
                
                if len(profile.code_postal) != 5:
                    messages.error(request, 'Le code postal doit contenir 5 chiffres.')
                    return render(request, 'complete_profile.html', {'form': form})
            
            # Validation spécifique pour patient
            if user.role == User.PATIENT:
                if len(profile.numero_secu) != 15:
                    messages.error(request, 'Le numéro de sécurité sociale doit contenir 15 chiffres.')
                    return render(request, 'complete_profile.html', {'form': form})
            
            profile.save()
            messages.success(request, 'Votre profil a été complété avec succès!')


    else:
        if user.role == User.MEDECIN:
            form = MedecinProfileForm(instance=profile)
        else:
            form = PatientProfileForm(instance=profile)
    
    return render(request, 'complete_profile.html', {
        'form': form,
        'profile': profile
    })


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('redirect_profile')  # On utilise redirect_profile au lieu de redirect_after_login
            else:
                messages.error(request, 'Email ou mot de passe incorrect.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def redirect_profile(request):
    user = request.user
    # Vérifier si le profil est déjà complet
    if user.role == User.MEDECIN:
        profile = get_object_or_404(Medecin, user=user)
        if profile.numero_rpps:  # Si le profil est déjà complet
            return redirect("doctor:doctor_dashboard")
    else:
        profile = get_object_or_404(Patient, user=user)
        if profile.numero_secu:  # Si le profil est déjà complet
            return redirect("patient:patient_dashboard")
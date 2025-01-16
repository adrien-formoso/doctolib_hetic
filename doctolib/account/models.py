from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    PATIENT = 'patient'
    MEDECIN = 'medecin'
    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (MEDECIN, 'Médecin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_rpps = models.CharField(max_length=11, unique=True)
    adresse = models.CharField(max_length=255)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=5)
    presentation = models.TextField(blank=True)
    prix_consultation = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    numero_secu = models.CharField(max_length=15, unique=True)
    medecin_traitant = models.ForeignKey(Medecin, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.user.get_full_name()
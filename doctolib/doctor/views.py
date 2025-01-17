from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def show_doctor_dashboard(requests):
    return render(requests,"patient_dashboard.html")
    pass

@login_required
def add_ecg():
    pass
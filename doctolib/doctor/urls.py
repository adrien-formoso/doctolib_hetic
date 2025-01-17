from django.urls import path
from . import views

app_name = 'doctor'
urlpatterns = [path("", views.show_doctor_dashboard, name="doctor_dashboard"),
               
               
                ]
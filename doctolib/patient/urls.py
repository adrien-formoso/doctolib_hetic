from django.urls import path
from . import views

app_name = 'patient'
urlpatterns = [path("patient_dashboard/", views.show_patient_dashboard, name="patient_dashboard"),
               path("patient_add_ecg/",views.add_ecg,name="patient_add_ecg")
               
               
                ]

LOGOUT_REDIRECT_URL = 'account:login'
AUTH_USER_MODEL = 'account.User'
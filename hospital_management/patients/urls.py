from django.urls import path
from . import views

# Define the namespace for reverse URL lookups
app_name = 'patients'

urlpatterns = [
    path('', views.patient_list, name='list'),  # List all patients
    path('create/', views.patient_create, name='create'),  # Create a new patient
    path('<int:pk>/edit/', views.patient_edit, name='edit'),  # Edit patient
    path('<int:pk>/delete/', views.patient_delete, name='delete'),  # Delete patient
]

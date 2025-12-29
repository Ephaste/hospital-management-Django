from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from patients.models import Patient

@login_required(login_url='login')
def dashboard_home(request):
    total_patients = Patient.objects.count()
    recent_patients = Patient.objects.order_by('-created_at')[:5]  # latest 5 patients

    context = {
        'total_patients': total_patients,
        'recent_patients': recent_patients,
    }

    return render(request, 'dashboard/dashboard_home.html', context)

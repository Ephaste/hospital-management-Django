from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from .forms import PatientForm  # We'll create this form to handle Patient data
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required(login_url='login')
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients:list')
    else:
        form = PatientForm()
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required(login_url='login')
def patient_edit(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patients:list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patients/patient_form.html', {'form': form})

@login_required(login_url='login')
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        return redirect('patients:list')
    return render(request, 'patients/patient_confirm_delete.html', {'patient': patient})

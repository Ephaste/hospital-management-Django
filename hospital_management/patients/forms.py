from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 
            'last_name', 
            'gender', 
            'date_of_birth', 
            'phone', 
            'address', 
            'status'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'gender': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded px-3 py-2 w-full'}),
            'phone': forms.TextInput(attrs={'class': 'border rounded px-3 py-2 w-full'}),
            'address': forms.Textarea(attrs={'class': 'border rounded px-3 py-2 w-full', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'border rounded px-3 py-2 w-full'}),
        }

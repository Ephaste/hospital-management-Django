from django.contrib import admin
from .models import Appointment
from accounts.models import CustomUser
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'nurse', 'appointment_date', 'status')
    list_filter = ('status', 'doctor', 'nurse')
    search_fields = ('patient__name', 'doctor__username', 'nurse__username')

admin.site.register(Appointment, AppointmentAdmin)

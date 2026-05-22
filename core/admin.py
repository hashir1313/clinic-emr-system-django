from django.contrib import admin
from .models import Patient, Visit, Prescription, ClinicInfo


@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'doctor_name', 'phone']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'age', 'gender', 'phone', 'created_at']
    search_fields = ['full_name', 'phone', 'patient_id']
    list_filter = ['gender', 'blood_group']


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'visit_date', 'follow_up_date']
    list_filter = ['visit_date']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'visit', 'created_at']

from django.contrib import admin
from .models import Patient, Visit, Prescription, ClinicInfo, Invoice, InvoiceItem


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


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'patient', 'total_amount', 'paid_amount', 'payment_status', 'issue_date']
    list_filter = ['payment_status', 'issue_date']
    search_fields = ['invoice_id', 'patient__full_name']
    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'invoice', 'quantity', 'unit_price', 'total_price']

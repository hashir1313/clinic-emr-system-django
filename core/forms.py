from django import forms
from .models import Patient, Visit, Prescription, ClinicInfo, Invoice, InvoiceItem
from django.contrib.auth.forms import AuthenticationForm
from decimal import Decimal


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400',
        'placeholder': 'Username',
        'autofocus': True,
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400',
        'placeholder': 'Password',
    }))


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['full_name', 'age', 'gender', 'phone', 'address', 'blood_group', 'allergies', 'medical_history']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'placeholder': 'Full Name'}),
            'age': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'placeholder': 'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 3, 'placeholder': 'Address'}),
            'blood_group': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'allergies': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 2, 'placeholder': 'List known allergies'}),
            'medical_history': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 3, 'placeholder': 'Medical history'}),
        }


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['symptoms', 'diagnosis', 'notes', 'follow_up_date']
        widgets = {
            'symptoms': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 3, 'placeholder': 'Symptoms'}),
            'diagnosis': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 3, 'placeholder': 'Diagnosis'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 3, 'placeholder': 'Additional notes'}),
            'follow_up_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'type': 'date'}),
        }


class ClinicForm(forms.ModelForm):
    class Meta:
        model = ClinicInfo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 3}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'doctor_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
        }


class InvoiceForm(forms.ModelForm):
    patient = forms.ModelChoiceField(
        queryset=Patient.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
        label='Patient'
    )

    class Meta:
        model = Invoice
        fields = ['patient', 'visit', 'due_date', 'consultation_fee', 'discount', 'tax', 'paid_amount', 'notes']
        widgets = {
            'visit': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'due_date': forms.DateInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'type': 'date'}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'step': '0.01'}),
            'discount': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'step': '0.01'}),
            'tax': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'step': '0.01'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.patient_id:
            self.fields['patient'].initial = self.instance.patient
            self.fields['patient'].disabled = True
            self.fields['visit'].queryset = self.instance.patient.visits.all()


class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['item_type', 'item_name', 'description', 'quantity', 'unit_price']
        widgets = {
            'item_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400'}),
            'item_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'placeholder': 'Item name'}),
            'description': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'placeholder': 'Optional description'}),
            'quantity': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'value': 1}),
            'unit_price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400', 'step': '0.01'}),
        }

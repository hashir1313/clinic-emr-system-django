from django import forms
from .models import Patient, Visit, Prescription, ClinicInfo
from django.contrib.auth.forms import AuthenticationForm


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

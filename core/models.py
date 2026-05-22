from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class ClinicInfo(models.Model):
    name = models.CharField(max_length=200, default="My Clinic")
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    doctor_name = models.CharField(max_length=200, default="Dr. Name")
    doctor_signature = models.ImageField(upload_to='signatures/', blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)

    class Meta:
        verbose_name = "Clinic Information"
        verbose_name_plural = "Clinic Information"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.name


class Patient(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]
    GENDERS = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    patient_id = models.CharField(max_length=20, unique=True, editable=False)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(150)])
    gender = models.CharField(max_length=1, choices=GENDERS)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS, blank=True)
    allergies = models.TextField(blank=True, help_text="List known allergies")
    medical_history = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last = Patient.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.patient_id = f"P{next_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.patient_id})"


class Visit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    follow_up_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-visit_date']

    def __str__(self):
        return f"Visit {self.id} - {self.patient.full_name} - {self.visit_date.date()}"


class Prescription(models.Model):
    visit = models.OneToOneField(Visit, on_delete=models.CASCADE, related_name='prescription')
    image = models.ImageField(upload_to='prescriptions/images/', blank=True, null=True)
    canvas_json = models.TextField(blank=True, help_text="Fabric.js canvas JSON stored in DB")
    json_file = models.FileField(upload_to='prescriptions/json/', blank=True, null=True, help_text="Canvas JSON saved as file on disk")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for Visit {self.visit.id}"


class Invoice(models.Model):
    PAYMENT_STATUS = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
    ]

    invoice_id = models.CharField(max_length=20, unique=True, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    visit = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='unpaid')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-issue_date', '-created_at']

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last = Invoice.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.invoice_id = f"INV-{next_id:04d}"
        self.remaining_amount = self.total_amount - self.paid_amount
        if self.remaining_amount <= 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'
        super().save(*args, **kwargs)

    def calculate_totals(self):
        items_total = self.items.aggregate(total=models.Sum('total_price'))['total'] or Decimal('0.00')
        self.subtotal = items_total + self.consultation_fee
        self.total_amount = self.subtotal - self.discount + self.tax
        self.remaining_amount = self.total_amount - self.paid_amount
        if self.remaining_amount <= 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'

    def __str__(self):
        return f"{self.invoice_id} - {self.patient.full_name}"


class InvoiceItem(models.Model):
    ITEM_TYPES = [
        ('consultation', 'Consultation'),
        ('procedure', 'Procedure'),
        ('medicine', 'Medicine'),
        ('lab', 'Lab'),
        ('other', 'Other'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPES, default='other')
    item_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = Decimal(str(self.quantity)) * self.unit_price
        super().save(*args, **kwargs)
        self.invoice.calculate_totals()
        self.invoice.save()

    def __str__(self):
        return f"{self.item_name} x{self.quantity}"

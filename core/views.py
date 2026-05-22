import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Patient, Visit, Prescription, ClinicInfo, Invoice, InvoiceItem
from .forms import PatientForm, VisitForm, ClinicForm, InvoiceForm, InvoiceItemForm
from django.db.models import Sum, Count, Q, DecimalField
from django.db.models.functions import TruncMonth
from decimal import Decimal
from utils.helpers import save_prescription_files, delete_prescription_files
from utils.printing import render_print_html


def setup(request):
    if User.objects.filter(is_superuser=True).exists():
        return redirect('login')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')
        if not username or not password:
            messages.error(request, 'All fields are required.')
        elif password != confirm:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
        else:
            User.objects.create_superuser(username=username, password=password)
            messages.success(request, 'Admin account created. Please log in.')
            return redirect('login')
    return render(request, 'core/setup.html')


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_visits = Visit.objects.count()
    total_earnings = Invoice.objects.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    total_paid = Invoice.objects.aggregate(total=Sum('paid_amount'))['total'] or Decimal('0.00')
    pending_payments = Invoice.objects.filter(payment_status__in=['unpaid', 'partial']).aggregate(total=Sum('remaining_amount'))['total'] or Decimal('0.00')
    paid_count = Invoice.objects.filter(payment_status='paid').count()
    unpaid_count = Invoice.objects.filter(payment_status__in=['unpaid', 'partial']).count()
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    recent_visits = Visit.objects.select_related('patient').order_by('-visit_date')[:5]
    recent_invoices = Invoice.objects.select_related('patient').order_by('-issue_date')[:5]
    context = {
        'total_patients': total_patients,
        'total_visits': total_visits,
        'total_earnings': total_earnings,
        'total_paid': total_paid,
        'pending_payments': pending_payments,
        'paid_count': paid_count,
        'unpaid_count': unpaid_count,
        'recent_patients': recent_patients,
        'recent_visits': recent_visits,
        'recent_invoices': recent_invoices,
        'section': 'dashboard',
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def patient_list(request):
    patients = Patient.objects.all()
    query = request.GET.get('q', '')
    if query:
        patients = patients.filter(
            Q(full_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(patient_id__icontains=query)
        )
    context = {
        'patients': patients,
        'query': query,
        'section': 'patients',
    }
    return render(request, 'core/patient_list.html', context)


@login_required
def patient_search(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(
        Q(full_name__icontains=query) |
        Q(phone__icontains=query) |
        Q(patient_id__icontains=query)
    ) if query else Patient.objects.none()
    return render(request, 'core/patient_list.html', {
        'patients': patients,
        'query': query,
        'section': 'patients',
    })


@login_required
def htmx_patient_search(request):
    query = request.GET.get('q', '')
    patients = Patient.objects.filter(
        Q(full_name__icontains=query) |
        Q(phone__icontains=query) |
        Q(patient_id__icontains=query)
    ) if query else Patient.objects.all()
    return render(request, 'core/_patient_table.html', {
        'patients': patients,
    })


@login_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient created successfully.')
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'core/patient_form.html', {
        'form': form,
        'title': 'Add Patient',
        'section': 'patients',
    })


@login_required
def patient_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Patient updated successfully.')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'core/patient_form.html', {
        'form': form,
        'patient': patient,
        'title': 'Edit Patient',
        'section': 'patients',
    })


@login_required
def patient_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('patient_list')
    return render(request, 'core/patient_confirm_delete.html', {
        'patient': patient,
        'section': 'patients',
    })


@login_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    visits = patient.visits.select_related('prescription').all()
    invoices = patient.invoices.all()
    total_billed = invoices.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    total_paid = invoices.aggregate(total=Sum('paid_amount'))['total'] or Decimal('0.00')
    pending_due = invoices.filter(payment_status__in=['unpaid', 'partial']).aggregate(total=Sum('remaining_amount'))['total'] or Decimal('0.00')
    return render(request, 'core/patient_detail.html', {
        'patient': patient,
        'visits': visits,
        'invoices': invoices,
        'total_billed': total_billed,
        'total_paid': total_paid,
        'pending_due': pending_due,
        'section': 'patients',
    })


@login_required
def visit_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.patient = patient
            visit.save()
            messages.success(request, 'Visit created successfully.')
            return redirect('prescription_drawing', visit_pk=visit.pk)
    else:
        form = VisitForm()
    return render(request, 'core/visit_form.html', {
        'form': form,
        'patient': patient,
        'title': 'New Visit',
        'section': 'visits',
    })


@login_required
def visit_update(request, pk):
    visit = get_object_or_404(Visit.objects.select_related('patient'), pk=pk)
    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Visit updated successfully.')
            return redirect('visit_detail', pk=visit.pk)
    else:
        form = VisitForm(instance=visit)
    return render(request, 'core/visit_form.html', {
        'form': form,
        'patient': visit.patient,
        'visit': visit,
        'title': 'Edit Visit',
        'section': 'visits',
    })


@login_required
def visit_delete(request, pk):
    visit = get_object_or_404(Visit.objects.select_related('patient'), pk=pk)
    patient_pk = visit.patient.pk
    if request.method == 'POST':
        if hasattr(visit, 'prescription'):
            delete_prescription_files(visit.prescription)
        visit.delete()
        messages.success(request, 'Visit deleted successfully.')
        return redirect('patient_detail', pk=patient_pk)
    return render(request, 'core/visit_confirm_delete.html', {
        'visit': visit,
        'section': 'visits',
    })


@login_required
def visit_detail(request, pk):
    visit = get_object_or_404(Visit.objects.select_related('patient'), pk=pk)
    prescription = getattr(visit, 'prescription', None)
    return render(request, 'core/visit_detail.html', {
        'visit': visit,
        'prescription': prescription,
        'section': 'visits',
    })


@login_required
def prescription_drawing(request, visit_pk):
    visit = get_object_or_404(Visit.objects.select_related('patient'), pk=visit_pk)
    prescription = getattr(visit, 'prescription', None)
    return render(request, 'core/prescription_drawing.html', {
        'visit': visit,
        'prescription': prescription,
        'section': 'prescriptions',
    })


@require_POST
@login_required
def prescription_save(request, visit_pk):
    try:
        data = json.loads(request.body)
        canvas_image = data.get('canvas_image', '')
        canvas_json = data.get('canvas_json', '')

        result = save_prescription_files(canvas_image, canvas_json, visit_pk)
        if result:
            return JsonResponse({'status': 'ok', 'message': 'Prescription saved.'})
        return JsonResponse({'status': 'error', 'message': 'Visit not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


@login_required
def prescription_load(request, visit_pk):
    visit = get_object_or_404(Visit, pk=visit_pk)
    prescription = getattr(visit, 'prescription', None)
    if prescription and prescription.canvas_json:
        try:
            data = json.loads(prescription.canvas_json)
            return JsonResponse({'status': 'ok', 'canvas_json': data})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid canvas data.'}, status=400)
    return JsonResponse({'status': 'empty', 'canvas_json': None})


@login_required
def visit_print(request, pk):
    visit = get_object_or_404(Visit.objects.select_related('patient'), pk=pk)
    html = render_print_html(visit)
    return HttpResponse(html)


@login_required
def clinic_settings(request):
    clinic = ClinicInfo.get()
    if request.method == 'POST':
        form = ClinicForm(request.POST, request.FILES, instance=clinic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Settings saved successfully.')
            return redirect('clinic_settings')
    else:
        form = ClinicForm(instance=clinic)
    return render(request, 'core/clinic_settings.html', {
        'form': form,
        'clinic': clinic,
        'section': 'settings',
    })


@login_required
def invoice_list(request):
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    invoices = Invoice.objects.select_related('patient').all()
    if query:
        invoices = invoices.filter(
            Q(invoice_id__icontains=query) |
            Q(patient__full_name__icontains=query)
        )
    if status_filter:
        invoices = invoices.filter(payment_status=status_filter)
    total_earnings = invoices.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    total_paid = invoices.aggregate(total=Sum('paid_amount'))['total'] or Decimal('0.00')
    context = {
        'invoices': invoices,
        'query': query,
        'status_filter': status_filter,
        'total_earnings': total_earnings,
        'total_paid': total_paid,
        'section': 'billing',
    }
    return render(request, 'core/invoice_list.html', context)


@login_required
def invoice_create(request, patient_pk=None, visit_pk=None):
    patient = None
    visit = None
    if patient_pk:
        patient = get_object_or_404(Patient, pk=patient_pk)
    if visit_pk:
        visit = get_object_or_404(Visit.objects.select_related('patient'), pk=visit_pk)
        patient = visit.patient

    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            if 'patient' in form.cleaned_data and form.cleaned_data['patient']:
                invoice.patient = form.cleaned_data['patient']
            invoice.save()
            messages.success(request, 'Invoice created. Add items now.')
            return redirect('invoice_update', pk=invoice.pk)
    else:
        initial = {}
        if visit:
            initial['visit'] = visit
        if patient:
            initial['patient'] = patient
        form = InvoiceForm(initial=initial)
        if patient:
            form.fields['visit'].queryset = patient.visits.all()

    return render(request, 'core/invoice_form.html', {
        'form': form,
        'patient': patient,
        'visit': visit,
        'section': 'billing',
    })


@login_required
def invoice_update(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('patient'), pk=pk)
    items = invoice.items.all()

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated.')
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(instance=invoice)
        form.fields['visit'].queryset = invoice.patient.visits.all()

    return render(request, 'core/invoice_form.html', {
        'form': form,
        'invoice': invoice,
        'items': items,
        'patient': invoice.patient,
        'section': 'billing',
    })


@require_POST
@login_required
def invoice_add_item(request, invoice_pk):
    invoice = get_object_or_404(Invoice, pk=invoice_pk)
    form = InvoiceItemForm(request.POST)
    if form.is_valid():
        item = form.save(commit=False)
        item.invoice = invoice
        item.save()
        messages.success(request, 'Item added.')
    else:
        for err in form.errors.values():
            messages.error(request, err)
    return redirect('invoice_update', pk=invoice.pk)


@login_required
def invoice_delete_item(request, invoice_pk, item_pk):
    item = get_object_or_404(InvoiceItem, pk=item_pk, invoice_id=invoice_pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item removed.')
    return redirect('invoice_update', pk=invoice_pk)


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('patient', 'visit'), pk=pk)
    items = invoice.items.all()
    return render(request, 'core/invoice_detail.html', {
        'invoice': invoice,
        'items': items,
        'section': 'billing',
    })


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    patient_pk = invoice.patient.pk
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, 'Invoice deleted.')
        return redirect('patient_detail', pk=patient_pk)
    return render(request, 'core/invoice_confirm_delete.html', {
        'invoice': invoice,
        'section': 'billing',
    })


@login_required
def invoice_print(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('patient', 'visit'), pk=pk)
    items = invoice.items.all()
    clinic = ClinicInfo.get()
    from django.template.loader import render_to_string
    html = render_to_string('core/print_invoice.html', {
        'invoice': invoice,
        'items': items,
        'clinic': clinic,
        'media_url': settings.MEDIA_URL,
    })
    return HttpResponse(html)

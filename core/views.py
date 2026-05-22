import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from .models import Patient, Visit, Prescription, ClinicInfo
from .forms import PatientForm, VisitForm, ClinicForm
from utils.helpers import save_prescription_files, delete_prescription_files
from utils.printing import generate_visit_pdf


def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_visits = Visit.objects.count()
    recent_patients = Patient.objects.order_by('-created_at')[:5]
    recent_visits = Visit.objects.select_related('patient').order_by('-visit_date')[:5]
    context = {
        'total_patients': total_patients,
        'total_visits': total_visits,
        'recent_patients': recent_patients,
        'recent_visits': recent_visits,
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
    return render(request, 'core/patient_detail.html', {
        'patient': patient,
        'visits': visits,
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
    pdf = generate_visit_pdf(visit)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="visit_{visit.id}.pdf"'
    return response


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

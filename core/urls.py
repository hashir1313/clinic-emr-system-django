from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('setup/', views.setup, name='setup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_create, name='patient_create'),
    path('patients/<int:pk>/edit/', views.patient_update, name='patient_update'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/search/', views.patient_search, name='patient_search'),

    # Visits
    path('patients/<int:patient_pk>/visits/add/', views.visit_create, name='visit_create'),
    path('visits/<int:pk>/edit/', views.visit_update, name='visit_update'),
    path('visits/<int:pk>/delete/', views.visit_delete, name='visit_delete'),
    path('visits/<int:pk>/', views.visit_detail, name='visit_detail'),

    # Prescription
    path('visits/<int:visit_pk>/prescription/', views.prescription_drawing, name='prescription_drawing'),
    path('visits/<int:visit_pk>/prescription/save/', views.prescription_save, name='prescription_save'),
    path('visits/<int:visit_pk>/prescription/load/', views.prescription_load, name='prescription_load'),

    # Printing
    path('visits/<int:pk>/print/', views.visit_print, name='visit_print'),

    # Settings
    path('settings/', views.clinic_settings, name='clinic_settings'),

    # HTMX search
    path('htmx/patient-search/', views.htmx_patient_search, name='htmx_patient_search'),

    # Billing / Invoices
    path('billing/', views.invoice_list, name='invoice_list'),
    path('billing/create/', views.invoice_create, name='invoice_create'),
    path('billing/create/<int:patient_pk>/', views.invoice_create, name='invoice_create_for_patient'),
    path('billing/create/<int:patient_pk>/<int:visit_pk>/', views.invoice_create, name='invoice_create_for_visit'),
    path('billing/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('billing/<int:pk>/edit/', views.invoice_update, name='invoice_update'),
    path('billing/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),
    path('billing/<int:pk>/print/', views.invoice_print, name='invoice_print'),
    path('billing/<int:invoice_pk>/items/add/', views.invoice_add_item, name='invoice_add_item'),
    path('billing/<int:invoice_pk>/items/<int:item_pk>/delete/', views.invoice_delete_item, name='invoice_delete_item'),
]

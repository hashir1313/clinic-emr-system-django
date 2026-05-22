import os
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse

try:
    from weasyprint import HTML
    HAS_WEASYPRINT = True
except (ImportError, OSError):
    HAS_WEASYPRINT = False


def generate_visit_pdf(visit):
    from core.models import ClinicInfo
    clinic = ClinicInfo.get()

    html_string = render_to_string('core/print_visit.html', {
        'visit': visit,
        'clinic': clinic,
        'prescription': getattr(visit, 'prescription', None),
        'static_url': settings.STATIC_URL,
        'media_url': settings.MEDIA_URL,
    })

    if HAS_WEASYPRINT:
        return HTML(string=html_string).write_pdf()

    return None


def render_print_html(visit):
    from core.models import ClinicInfo
    clinic = ClinicInfo.get()

    return render_to_string('core/print_visit.html', {
        'visit': visit,
        'clinic': clinic,
        'prescription': getattr(visit, 'prescription', None),
        'static_url': settings.STATIC_URL,
        'media_url': settings.MEDIA_URL,
    })

from django.template.loader import render_to_string
from django.conf import settings
from weasyprint import HTML
import os


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

    pdf_file = HTML(string=html_string).write_pdf()

    return pdf_file

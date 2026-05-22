import os
import json
from django.conf import settings
from django.core.files.base import ContentFile
import base64
import uuid


def save_prescription_files(canvas_image_data, canvas_json, visit_id):
    from core.models import Prescription, Visit
    try:
        visit = Visit.objects.get(id=visit_id)
    except Visit.DoesNotExist:
        return None

    presc, created = Prescription.objects.get_or_create(visit=visit)

    if canvas_image_data and canvas_image_data.startswith('data:image'):
        fmt, imgstr = canvas_image_data.split(';base64,')
        ext = fmt.split('/')[-1]
        image_data = base64.b64decode(imgstr)
        filename = f"prescription_{visit_id}_{uuid.uuid4().hex[:8]}.{ext}"
        presc.image.save(filename, ContentFile(image_data), save=False)

    if canvas_json:
        presc.canvas_json = canvas_json
        json_filename = f"prescription_{visit_id}_{uuid.uuid4().hex[:8]}.json"
        presc.json_file.save(json_filename, ContentFile(canvas_json.encode('utf-8')), save=False)

    presc.save()
    return presc


def delete_prescription_files(prescription):
    for f in [prescription.image, prescription.json_file]:
        if f and f.name:
            path = os.path.join(settings.MEDIA_ROOT, f.name)
            if os.path.exists(path):
                os.remove(path)
    prescription.delete()

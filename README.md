# Clinic EMR System

A fully offline-capable clinic management system for single-doctor practices. Manage patient records, visits, handwritten digital prescriptions, billing, and printable documents — all without internet access.

## Features

### Patient Management
- Create, edit, delete patients
- Search by name, phone, or patient ID
- Medical history, allergies, blood group tracking

### Visit Management
- Create visits linked to patients
- Record symptoms, diagnosis, notes, follow-up dates
- Full visit history timeline per patient

### Digital Prescriptions
- Handwritten prescription drawing with stylus/tablet support
- Fabric.js-based canvas with pen/eraser, undo/redo, brush size/color
- Pointer events for iPad, S-Pen, Surface devices
- Save/load/restore previous prescriptions as editable JSON
- Prescriptions stored as both images (PNG) and editable JSON files

### Billing & Invoices
- Create invoices linked to patient visits
- Add line items (consultation, procedures, medicines, lab, custom)
- Auto-calculated subtotal, discount, tax, total, remaining balance
- Payment status tracking (paid, unpaid, partially paid)
- Search and filter invoices
- Printable invoices

### Printing
- Professional A4 printable visit reports
- Professional A4 printable invoices
- Auto-triggers browser print dialog
- Works fully offline

### Dashboard
- Total patients, visits, earnings overview
- Recent patients, visits, invoices
- Quick actions for common tasks

### Offline-First
- Zero internet dependency
- All libraries served locally (no CDN)
- SQLite database — single file, portable
- Entire application runs from one folder

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Django 6.0 |
| Database | SQLite |
| Frontend | Django Templates, Tailwind CSS, Vanilla JS |
| Dynamic Interactions | HTMX |
| Drawing | Fabric.js |
| Printing | Browser native print (HTML/CSS) |
| Icons/UI | Tailwind CSS |

## Project Structure

```
clinic-emr-system-django/
├── clinic_emr/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                    # Main application
│   ├── models.py            # Patient, Visit, Prescription, Invoice, etc.
│   ├── views.py             # All views
│   ├── forms.py             # All forms
│   ├── urls.py              # URL routing
│   └── admin.py             # Admin interface
├── templates/
│   ├── base.html            # Base layout
│   └── core/                # All page templates
│       ├── dashboard.html
│       ├── patient_list.html
│       ├── patient_detail.html
│       ├── visit_form.html
│       ├── prescription_drawing.html
│       ├── invoice_list.html
│       ├── invoice_form.html
│       ├── print_visit.html
│       ├── print_invoice.html
│       └── ...
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── vendor/              # Local copies of all JS/CSS libs
│       ├── htmx/
│       ├── fabric/
│       ├── alpine/
│       └── tailwind/
├── utils/
│   ├── helpers.py           # Prescription file management
│   └── printing.py          # Print HTML rendering
├── media/
│   ├── prescriptions/
│   │   ├── images/          # Prescription PNG files
│   │   └── json/            # Prescription JSON files
│   └── patient_documents/
├── manage.py
├── requirements.txt
├── .gitignore
└── Procfile
```

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd clinic-emr-system-django

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### First Login
1. Navigate to `http://localhost:8000/`
2. Log in with the admin credentials you created
3. Go to `/settings/` to configure clinic information
4. Start by adding a patient, then create a visit and prescription

## Usage

### Patients
- **Add**: Click "+ Add Patient" on the Patients page
- **Search**: Use the search bar — searches by name, phone, or patient ID
- **View**: Click a patient name to see full profile, visit history, and invoices

### Visits
- **Create**: From patient profile, click "+ New Visit"
- **Record**: Enter symptoms, diagnosis, notes, and follow-up date
- **Prescription**: After creating a visit, you're taken to the prescription drawing page

### Prescriptions
- **Draw**: Use the canvas with pen/eraser tools
- **Save**: Click "Save" to store the prescription as PNG + editable JSON
- **Restore**: Open a previous visit's prescription to continue editing
- **Shortcuts**: Ctrl+Z (undo), Ctrl+Shift+Z (redo), Ctrl+S (save)

### Billing
- **Create Invoice**: From patient profile click "+ Invoice" or from Billing page
- **Add Items**: After creating an invoice, add line items (consultation, medicines, etc.)
- **Auto-calculations**: Totals, discounts, tax, and remaining balance update automatically
- **Print**: Click "Print" to generate a printable A4 invoice

### Printing
- **Visit Report**: Click "Print" on any visit
- **Invoice**: Click "Print" on any invoice
- Both auto-open your browser's print dialog

## Deployment

### Render.com
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect repository
4. Set Build Command: `pip install -r requirements.txt`
5. Set Start Command: `python manage.py migrate --noinput && gunicorn clinic_emr.wsgi --bind 0.0.0.0:$PORT`
6. Deploy

### Fully Offline
No internet is needed once the application is running. All frontend libraries are included in `/static/vendor/`. The SQLite database stores everything locally.

## Security
- Authentication required for all pages
- No public registration — admin account created manually
- CSRF protection on all forms
- Session-based authentication

## License
MIT

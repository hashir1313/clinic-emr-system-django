# Clinic EMR System

A fully offline-capable clinic management system for single-doctor practices. Manage patient records, visits, handwritten digital prescriptions, billing/invoicing, and printable documents — zero internet required.

## Features

### Patient Management
- Create, edit, delete patient records
- Search by name, phone, or auto-generated patient ID
- Store demographics, contact, blood group, allergies, medical history

### Visit Management
- Create visits linked to patients with auto-generated timestamps
- Record symptoms, diagnosis, notes, and follow-up dates
- Full chronological visit history per patient

### Digital Prescriptions
- **Handwritten prescription drawing** using Fabric.js canvas
- Pen/eraser tools, brush size/color controls, undo/redo
- Full **pointer events** support for stylus/tablet (iPad, S-Pen, Surface)
- Save prescriptions as both **PNG images** and **editable JSON files**
- Reload and edit previous prescriptions from any visit
- Keyboard shortcuts: `Ctrl+Z` undo, `Ctrl+Shift+Z` redo, `Ctrl+S` save

### Billing & Invoices
- Create invoices linked to patients and optionally to specific visits
- Add line items: consultation fees, procedures, medicines, lab charges, custom items
- **Auto-calculated**: subtotal, discount, tax, grand total, paid amount, remaining balance
- Payment status tracking: **Paid / Unpaid / Partially Paid**
- Search and filter invoices by ID, patient name, date, or payment status
- Financial summary on dashboard (total earnings, collected, pending)

### Printing
- **Printable visit reports** — professional A4 layout with patient info, vitals, prescription image, doctor signature
- **Printable invoices** — professional A4 layout with itemized table, totals, payment status
- Auto-triggers browser print dialog on page load
- All printing works fully offline

### Dashboard
- Overview cards: total patients, visits, earnings, pending payments
- Recent patients, visits, and invoices with quick-action links
- Quick access to create patient, visit, or invoice

### Fully Offline
- **Zero CDN dependencies** — all libraries (HTMX, Fabric.js, Alpine.js, Tailwind, Lucide) served locally from `static/vendor/`
- **SQLite database** — single file, fully portable, no server setup
- Entire application runs from one folder, nothing leaves your machine

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | **Django 6.0** |
| Database | **SQLite** (zero-config, single file) |
| Frontend | Django Templates, **Tailwind CSS**, Vanilla JavaScript |
| Dynamic UI | **HTMX** (AJAX partial page updates) |
| Drawing | **Fabric.js** 5.x (prescription canvas) |
| Icons | **Lucide** |
| PDF | WeasyPrint (optional, gracefully degrades) |
| Styling | Tailwind CSS (utility-first, minimal custom CSS) |

## Project Structure

```
clinic-emr-system-django/
├── clinic_emr/                  # Django project configuration
│   ├── settings.py
│   ├── urls.py                  # Root URL config (includes core + admin)
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                        # Main application
│   ├── models.py                # 6 models (see below)
│   ├── views.py                 # 27 views
│   ├── forms.py                 # 6 forms
│   ├── urls.py                  # 30+ URL routes
│   ├── admin.py                 # Admin config for all models
│   ├── templatetags/
│   │   └── core_extras.py       # Custom template filters
│   └── migrations/              # 3 migration files
│
├── templates/
│   ├── base.html                # Main layout (nav, messages, scripts)
│   └── core/                    # 18 page templates
│       ├── login.html
│       ├── dashboard.html
│       ├── patient_list.html
│       ├── _patient_table.html  # HTMX partial
│       ├── patient_form.html
│       ├── patient_detail.html  # Profile + visit/invoice history
│       ├── patient_confirm_delete.html
│       ├── visit_form.html
│       ├── visit_detail.html
│       ├── visit_confirm_delete.html
│       ├── prescription_drawing.html  # Fabric.js canvas
│       ├── print_visit.html           # Printable A4 report
│       ├── invoice_list.html
│       ├── invoice_form.html
│       ├── invoice_detail.html
│       ├── invoice_confirm_delete.html
│       ├── print_invoice.html         # Printable A4 invoice
│       └── clinic_settings.html
│
├── static/
│   ├── css/style.css
│   ├── js/main.js
│   └── vendor/                   # All libraries (local, no CDN)
│       ├── htmx/
│       │   ├── htmx.min.js
│       │   └── json-enc.js
│       ├── fabric/fabric.min.js
│       ├── alpine/alpine.min.js
│       ├── tailwind/tailwind.min.css
│       └── lucide/
│           ├── lucide.min.js
│           └── lucide.js
│
├── utils/
│   ├── helpers.py                # Prescription file save/delete
│   └── printing.py               # Print HTML/PDF rendering
│
├── media/
│   ├── prescriptions/
│   │   ├── images/               # Prescription PNG files
│   │   └── json/                 # Prescription JSON files
│   └── patient_documents/
│
├── Setup/
│   ├── setup.bat                 # Windows one-click setup
│   └── setup.sh                  # Linux/Mac one-click setup
│
├── start-win.bat                 # Windows start script
├── start-linux.sh                # Linux/Mac start script
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Database Models

| Model | Key Fields | Purpose |
|-------|-----------|---------|
| **ClinicInfo** | name, address, phone, email, doctor_name, logo, signature | Singleton clinic settings |
| **Patient** | patient_id (auto: P0001), full_name, age, gender, phone, blood_group, allergies, medical_history | Patient records |
| **Visit** | patient (FK), visit_date, symptoms, diagnosis, notes, follow_up_date | Patient visits |
| **Prescription** | visit (OneToOne), image (PNG), canvas_json, json_file (JSON) | Digital prescriptions |
| **Invoice** | invoice_id (auto: INV-0001), patient, visit, subtotal, discount, tax, total, paid, remaining, payment_status | Billing |
| **InvoiceItem** | invoice (FK), item_type, item_name, quantity, unit_price, total_price (auto-calc) | Line items |

## Quick Start

### Prerequisites
- Python 3.10+
- pip
- git

### Windows
```batch
git clone https://github.com/hashir1313/clinic-emr-system-django
cd clinic-emr-system-django
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Or simply run `Setup/setup.bat` which does all of the above automatically.

### Linux / Mac
```bash
git clone https://github.com/hashir1313/clinic-emr-system-django
cd clinic-emr-system-django
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Or simply run `bash Setup/setup.sh` which does all of the above automatically.

### First Use
1. Open `http://localhost:8000/` and log in with your admin credentials
2. Go to **Settings** (`/settings/`) to configure your clinic name, address, doctor name, etc.
3. Click **Patients** to add your first patient
4. From the patient profile, create a **Visit** then write a **Prescription**
5. From any visit, click **Print** to generate a printable visit report
6. From any patient, click **+ Invoice** to create a bill with line items

## Usage Guide

### Patients
| Action | How |
|--------|-----|
| Add | Click "+ Add Patient" on Patients page |
| Search | Type in the search bar — searches name, phone, ID in real-time (HTMX) |
| View | Click patient name → profile with demographics, visit history, invoice history |
| Edit | Click "Edit" on patient profile |
| Delete | Click "Delete" on patient profile (confirmation required) |

### Visits
| Action | How |
|--------|-----|
| Create | Click "+ New Visit" on patient profile → fill symptoms, diagnosis, notes → auto-redirects to prescription |
| Edit | Click "Edit" on visit detail page |
| View | Click "View" on any visit in patient history |
| Print | Click "Print" → opens A4 printable report with auto-print dialog |

### Prescriptions
- Use the **Pen** tool to draw freehand on the canvas
- Switch to **Eraser** to remove strokes (click on them)
- Adjust **brush size** (slider) and **color** (color picker)
- **Undo/Redo** or use `Ctrl+Z` / `Ctrl+Shift+Z`
- Click **Save** to store as PNG + editable JSON
- Reopening a previous prescription loads the saved JSON — continue editing
- `Ctrl+S` shortcut to save

### Billing
| Action | How |
|--------|-----|
| Create Invoice | Click "+ Invoice" on patient profile, or "+ New Invoice" on Billing page |
| Add Items | After creating invoice, add line items (type, name, qty, price) |
| Update Payment | Edit invoice → change paid amount → status updates automatically |
| View | Click invoice ID to see full itemized breakdown |
| Print | Click "Print" → opens A4 printable invoice with auto-print dialog |
| Search | On Billing page, search by ID/name or filter by payment status |

### Auto-Calculations
- **Item total** = quantity × unit price (auto-calculated on save)
- **Subtotal** = sum of all item totals + consultation fee
- **Grand total** = subtotal − discount + tax
- **Remaining** = total − paid amount
- **Payment status**: remaining ≤ 0 → "Paid", paid > 0 → "Partial", otherwise "Unpaid"

## Setup Scripts

The project includes convenience scripts for first-time setup:

### `Setup/setup.bat` (Windows)
```batch
@echo off
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### `Setup/setup.sh` (Linux/Mac)
```bash
#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### `start-win.bat` (Windows — quick launch)
```batch
@echo off
git pull
call venv\Scripts\activate
python manage.py runserver
start http://localhost:8000
```

### `start-linux.sh` (Linux/Mac — quick launch)
```bash
#!/bin/bash
git pull
source venv/bin/activate
python manage.py runserver
xdg-open http://localhost:8000
```

## Deployment

### Render.com
1. Push code to GitHub
2. Create new **Web Service** on Render
3. Connect your repository
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `python manage.py migrate --noinput && gunicorn clinic_emr.wsgi --bind 0.0.0.0:$PORT`

## Offline-First Design

This application is designed to run **completely without internet access**:

- **All frontend libraries** are vendored locally in `static/vendor/` — no CDN calls
- **SQLite database** stores everything in a single `db.sqlite3` file — no database server
- **Local file storage** for prescription images and JSON files in `media/`
- **Browser-native printing** — no cloud print services
- **WeasyPrint** is optional; if the system GTK libraries aren't available, printing falls back to HTML + browser print

## Security

- **Authentication required** for all pages (login redirect)
- **No public registration** — admin account created via `createsuperuser` or `Setup/setup` scripts
- **CSRF protection** on all forms
- **Session-based authentication**
- **Route protection** via `@login_required` decorator on all views

## Future-Proof Architecture

The codebase is structured for future expansion:

- **Billing**: Ready for inventory integration, multi-doctor billing, GST/VAT, export features
- **Prescriptions**: JSON storage enables cloud sync if ever needed
- **Models**: Clean FK relationships allow extending with insurance, appointments, lab results
- **Utils**: Service layer pattern separates business logic from views

from flask import Flask, request, render_template
from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
from config.settings import Config
from src.extensions import db, migrate
from flask_sqlalchemy import SQLAlchemy
# Use package-relative imports so modules resolve when running as `src.app`
from .models import Patient, Doctor, Appointment, MedicalRecord

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('//Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/templates/home.html')
    def home():
        return render_template('home.html')

    @app.route('/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/templates/patients.html')
    def patients():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = Patient.query

        if search:
            # Simple search on first_name, last_name, or phone
            query = query.filter(
                (Patient.first_name.ilike(f'%{search}%')) |
                (Patient.last_name.ilike(f'%{search}%')) |
                (Patient.phone.ilike(f'%{search}%'))
            )

        patients_paginated = query.order_by(Patient.id).paginate(page=page, per_page=10)
    
        return render_template('patients.html', patients=patients_paginated, search=search)

    # Create a new patient (form submission)
    @app.route('/patients/add', methods=['POST'])
    def add_patient():
        form = request.form
        try:
            dob = None
            if form.get('date_of_birth'):
                dob = None
                try:
                    dob = datetime.strptime(form.get('date_of_birth'), '%Y-%m-%d').date()
                except Exception:
                    dob = None

            next_appt = None
            if form.get('next_appointment'):
                try:
                    next_appt = datetime.strptime(form.get('next_appointment'), '%Y-%m-%d').date()
                except Exception:
                    next_appt = None

            patient = Patient(
                first_name=form.get('first_name', ''),
                last_name=form.get('last_name', ''),
                date_of_birth=dob or datetime.utcnow().date(),
                gender=form.get('gender'),
                blood_type=form.get('blood_type'),
                phone=form.get('phone'),
                email=form.get('email'),
                address=form.get('address'),
                emergency_contact=form.get('emergency_contact'),
                emergency_contact_phone=form.get('emergency_contact_phone'),
                insurance_provider=form.get('insurance_provider'),
                insurance_number=form.get('insurance_number'),
                allergies=form.get('allergies'),
                drug_interactions=form.get('drug_interactions'),
                past_medical_history=form.get('past_medical_history'),
                surgical_history=form.get('surgical_history'),
                family_medical_history=form.get('family_medical_history'),
                social_history=form.get('social_history'),
                immunizations=form.get('immunizations'),
                hospital_stays=form.get('hospital_stays'),
                next_appointment=next_appt,
                primary_physician=form.get('primary_physician'),
                incident_history=form.get('incident_history')
            )
            db.session.add(patient)
            db.session.commit()
        except Exception:
            db.session.rollback()
            # For simplicity, we ignore errors and redirect back; in production log/flash
        return redirect(url_for('patients'))

    @app.route('/patients/<int:patient_id>/update', methods=['POST'])
    def update_patient(patient_id):
        form = request.form
        patient = Patient.query.get_or_404(patient_id)
        try:
            if form.get('first_name') is not None:
                patient.first_name = form.get('first_name')
            if form.get('last_name') is not None:
                patient.last_name = form.get('last_name')
            if form.get('date_of_birth'):
                try:
                    patient.date_of_birth = datetime.strptime(form.get('date_of_birth'), '%Y-%m-%d').date()
                except Exception:
                    pass
            patient.gender = form.get('gender')
            patient.blood_type = form.get('blood_type')
            patient.phone = form.get('phone')
            patient.email = form.get('email')
            patient.address = form.get('address')
            patient.emergency_contact = form.get('emergency_contact')
            patient.emergency_contact_phone = form.get('emergency_contact_phone')
            patient.insurance_provider = form.get('insurance_provider')
            patient.insurance_number = form.get('insurance_number')
            patient.allergies = form.get('allergies')
            patient.drug_interactions = form.get('drug_interactions')
            patient.past_medical_history = form.get('past_medical_history')
            patient.surgical_history = form.get('surgical_history')
            patient.family_medical_history = form.get('family_medical_history')
            patient.social_history = form.get('social_history')
            patient.immunizations = form.get('immunizations')
            patient.hospital_stays = form.get('hospital_stays')
            if form.get('next_appointment'):
                try:
                    patient.next_appointment = datetime.strptime(form.get('next_appointment'), '%Y-%m-%d').date()
                except Exception:
                    pass
            patient.primary_physician = form.get('primary_physician')
            patient.incident_history = form.get('incident_history')
            db.session.commit()
        except Exception:
            db.session.rollback()
        return redirect(url_for('patients'))
# ----------------- Doctors -----------------
    @app.route('/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/templates/doctors.html')
    def doctors():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = Doctor.query
        if search:
            query = query.filter(
                (Doctor.name.ilike(f'%{search}%')) |
                (Doctor.specialty.ilike(f'%{search}%'))
            )

        doctors_paginated = query.order_by(Doctor.id).paginate(page=page, per_page=10)
        return render_template('doctors.html', doctors=doctors_paginated, search=search)

    # ----------------- Appointments -----------------
    @app.route('/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/templates/appointments.html')
    def appointments():
        page = request.args.get('page', 1, type=int)
        appointments_paginated = Appointment.query.order_by(Appointment.id).paginate(page=page, per_page=10)
        return render_template('appointments.html', appointments=appointments_paginated)

    # ----------------- Medical Records -----------------
    @app.route('/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/templates/medical_records.html')
    def medical_records():
        page = request.args.get('page', 1, type=int)
        records_paginated = MedicalRecord.query.order_by(MedicalRecord.id).paginate(page=page, per_page=10)
        return render_template('medical_records.html', records=records_paginated)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
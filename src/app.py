from flask import Flask, request, render_template, redirect, url_for, flash
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

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/patients', methods=['GET', 'POST'])
    def patients():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        query = Patient.query

        if search:
            # Simple search on first_name, last_name, or phone
            query = query.filter(
                (Patient.first_name.ilike(f'%{search}%')) |
                (Patient.last_name.ilike(f'%{search}%')) |
                (Patient.phone.ilike(f'%{search}%')) |
                (Patient.id.ilike(f'%{search}%'))
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

    @app.route("/patients/delete/<int:id>", methods=["POST"])
    def delete_patient(id):
        patient = Patient.query.get_or_404(id)
        db.session.delete(patient)
        db.session.commit()
        flash("Patient deleted successfully!", "info")
        return redirect(url_for('patients'))
        
    @app.route('/doctors')
    def doctors():
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '', type=str)

        # GET request: show doctors list
        query = Doctor.query
        if search:
            query = query.filter(
                (Doctor.first_name.ilike(f'%{search}%')) |
                (Doctor.last_name.ilike(f'%{search}%')) |
                (Doctor.specialization.ilike(f'%{search}%'))
            )

        doctors_paginated = query.order_by(Doctor.id).paginate(page=page, per_page=10)
        return render_template('doctors.html', doctors=doctors_paginated, search=search)

    # Create a new doctor (form submission)
    @app.route('/doctors/add', methods=['POST'])
    def add_doctor():
        form = request.form
        try:
            doctor = Doctor(
                first_name=form.get('first_name'),
                last_name=form.get('last_name'),
                specialization=form.get('specialization'),
                phone=form.get('phone'),
                email=form.get('email'),
                department=form.get('department'),
                status=form.get('status', 'Active')
            )
            db.session.add(doctor)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return redirect(url_for('doctors'))

    # Update an existing doctor (form submission)
    @app.route('/doctors/<int:doctor_id>/update', methods=['POST'])
    def update_doctor(doctor_id):
        form = request.form
        doctor = Doctor.query.get_or_404(doctor_id)
        try:
            doctor.first_name = form.get('first_name') or doctor.first_name
            doctor.last_name = form.get('last_name') or doctor.last_name
            doctor.specialization = form.get('specialization') or doctor.specialization
            doctor.phone = form.get('phone')
            doctor.email = form.get('email') or doctor.email
            doctor.department = form.get('department')
            doctor.status = form.get('status', 'Active')
            db.session.commit()
        except Exception:
            db.session.rollback()
        return redirect(url_for('doctors'))

    # Delete a doctor
    @app.route('/doctors/<int:doctor_id>/delete', methods=['POST'])
    def delete_doctor(doctor_id):
        doctor = Doctor.query.get_or_404(doctor_id)
        db.session.delete(doctor)
        db.session.commit()
        return redirect(url_for('doctors'))



    # ----------------- Appointments -----------------
    @app.route('/appointments')
    def appointments():
        page = request.args.get('page', 1, type=int)
        appointments_paginated = Appointment.query.order_by(Appointment.appointment_date.desc()).paginate(page=page, per_page=10)
        all_patients = Patient.query.all()
        all_doctors = Doctor.query.all()
        return render_template('appointments.html', appointments=appointments_paginated, all_patients=all_patients, all_doctors=all_doctors)

    @app.route('/appointments/add', methods=['POST'])
    def add_appointment():
        form = request.form
        try:
            appt_date = None
            if form.get('appointment_date'):
                try:
                    appt_date = datetime.strptime(form.get('appointment_date'), '%Y-%m-%dT%H:%M')
                except Exception:
                    pass
            
            appointment = Appointment(
                patient_id=int(form.get('patient_id')),
                doctor_id=int(form.get('doctor_id')),
                appointment_date=appt_date,
                status=form.get('status', 'Scheduled'),
                reason=form.get('reason')
            )
            db.session.add(appointment)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return redirect(url_for('appointments'))

    # ----------------- Medical Records -----------------
    @app.route('/medical_records')
    def medical_records():
        page = request.args.get('page', 1, type=int)
        records_paginated = MedicalRecord.query.order_by(MedicalRecord.id).paginate(page=page, per_page=10)
        all_patients = Patient.query.all()
        all_doctors = Doctor.query.all()
        return render_template('medical_records.html', records=records_paginated, all_patients=all_patients, all_doctors=all_doctors)

    @app.route('/medical_records/add', methods=['POST'])
    def add_medical_record():
        form = request.form
        try:
            medical_record = MedicalRecord(
                patient_id=int(form.get('patient_id')),
                doctor_id=int(form.get('doctor_id')) if form.get('doctor_id') else None,
                diagnosis=form.get('diagnosis'),
                treatment=form.get('treatment'),
                prescription=form.get('prescription'),
                test_results=form.get('test_results'),
                date_recorded=datetime.now()
            )
            db.session.add(medical_record)
            db.session.commit()
        except Exception:
            db.session.rollback()
        return redirect(url_for('medical_records'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
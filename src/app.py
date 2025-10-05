from flask import Flask, request, render_template
from config.settings import Config
from src.extensions import db, migrate
from flask_sqlalchemy import SQLAlchemy
from models import Patient, Doctor, Appointment, MedicalRecord, Staff, InventoryItem, Billing, Admin, Nurse
from src.models import *

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/__init__.py')
    def home():
        return render_template('home.html')

    @app.route('/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/src/models/patient.py')
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
# ----------------- Doctors -----------------
    @app.route('/doctors')
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
    @app.route('/appointments')
    def appointments():
        page = request.args.get('page', 1, type=int)
        appointments_paginated = Appointment.query.order_by(Appointment.id).paginate(page=page, per_page=10)
        return render_template('appointments.html', appointments=appointments_paginated)

    # ----------------- Medical Records -----------------
    @app.route('/medical-records')
    def medical_records():
        page = request.args.get('page', 1, type=int)
        records_paginated = MedicalRecord.query.order_by(MedicalRecord.id).paginate(page=page, per_page=10)
        return render_template('medical_records.html', records=records_paginated)

    # ----------------- Staff -----------------
    @app.route('/staff')
    def staff():
        page = request.args.get('page', 1, type=int)
        staff_paginated = Staff.query.order_by(Staff.id).paginate(page=page, per_page=10)
        return render_template('staff.html', staff=staff_paginated)

    # ----------------- Inventory -----------------
    @app.route('/inventory')
    def inventory():
        page = request.args.get('page', 1, type=int)
        inventory_paginated = InventoryItem.query.order_by(InventoryItem.id).paginate(page=page, per_page=10)
        return render_template('inventory.html', items=inventory_paginated)

    # ----------------- Billing -----------------
    @app.route('/billing')
    def billing():
        page = request.args.get('page', 1, type=int)
        billing_paginated = Billing.query.order_by(Billing.id).paginate(page=page, per_page=10)
        return render_template('billing.html', bills=billing_paginated)

    # ----------------- Admin -----------------
    @app.route('/admin')
    def admin():
        page = request.args.get('page', 1, type=int)
        admin_paginated = Admin.query.order_by(Admin.id).paginate(page=page, per_page=10)
        return render_template('admin.html', admins=admin_paginated)

    # ----------------- Nurses -----------------
    @app.route('/nurses')
    def nurses():
        page = request.args.get('page', 1, type=int)
        nurses_paginated = Nurse.query.order_by(Nurse.id).paginate(page=page, per_page=10)
        return render_template('nurses.html', nurses=nurses_paginated)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
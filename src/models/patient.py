from datetime import datetime
from src.extensions import db

ALL_DELETE_ORPHAN = "all, delete-orphan"

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    blood_type = db.Column(db.String(5), nullable=True)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(255))
    emergency_contact = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    insurance_number = db.Column(db.String(50), nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    drug_interactions = db.Column(db.Text, nullable=True)
    past_medical_history = db.Column(db.Text, nullable=True)
    surgical_history = db.Column(db.Text, nullable=True)
    family_medical_history = db.Column(db.Text, nullable=True)
    social_history = db.Column(db.Text, nullable=True)
    immunizations = db.Column(db.Text, nullable=True)
    hospital_stays = db.Column(db.Text, nullable=True)
    next_appointment = db.Column(db.Date, nullable=True)
    primary_physician = db.Column(db.String(100), nullable=True)
    incident_history = db.Column(db.Text, nullable=True)
    appointments = db.relationship("Appointment", back_populates="patient", cascade=ALL_DELETE_ORPHAN)
    medical_records = db.relationship("MedicalRecord", back_populates="patient", cascade=ALL_DELETE_ORPHAN)

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"

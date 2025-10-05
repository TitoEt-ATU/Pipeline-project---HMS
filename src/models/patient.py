from datetime import datetime
from src.extensions import db

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(255))
    emergency_contact = db.Column(db.String(100))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    medical_records = db.relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")
    bills = db.relationship("Billing", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"

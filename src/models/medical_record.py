from datetime import datetime
from src.extensions import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    diagnosis = db.Column(db.Text)
    treatment = db.Column(db.Text)
    prescription = db.Column(db.Text)
    test_results = db.Column(db.Text)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", back_populates="medical_records")
    doctor = db.relationship("Doctor")

    def __repr__(self):
        return f"<MedicalRecord {self.id} for Patient {self.patient_id}>"

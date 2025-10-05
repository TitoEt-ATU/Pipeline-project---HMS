from datetime import datetime
from src.extensions import db

class Billing(db.Model):
    __tablename__ = 'billing'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    paid_amount = db.Column(db.Float, default=0.0)
    payment_method = db.Column(db.String(50))  # Cash, Card, Insurance
    status = db.Column(db.String(20), default="Pending")  # Pending, Paid, Partially Paid
    billing_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    notes = db.Column(db.String(255))

    patient = db.relationship("Patient", back_populates="bills")

    def __repr__(self):
        return f"<Billing #{self.id} - Patient {self.patient_id} - {self.status}>"

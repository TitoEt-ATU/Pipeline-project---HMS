# src/load_csv.py
import pandas as pd
from app import app, db
from models import Patient

csv_file = "/Users/titoetimiri/Hospital Management System/Pipeline-project---HMS/patient_records_500_full_history.csv"

with app.app_context():
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        patient = Patient(
            first_name=row['First_Name'],
            last_name=row['Last_Name'],
            date_of_birth=row.get('Date_of_Birth'),
            gender=row.get('Gender'),
            blood_type=row.get('Blood_Type'),
            phone=row.get('Phone'),
            email=row.get('Email'),
            address=row.get('Address'),
            emergency_contact_name=row.get('Emergency_Contact_Name'),
            emergency_contact_phone=row.get('Emergency_Contact_Phone'),
            insurance_provider=row.get('Insurance_Provider'),
            insurance_number=row.get('Insurance_Number'),
            allergies=row.get('Allergies'),
            drug_interactions=row.get('Drug_Interactions'),
            past_medical_history=row.get('Past_Medical_History'),
            surgical_history=row.get('Surgical_History'),
            family_medical_history=row.get('Family_Medical_History'),
            social_history=row.get('Social_History'),
            immunizations=row.get('Immunizations'),
            hospital_stays=row.get('Hospital_Stays'),
            next_appointment=row.get('Next_Appointment'),
            primary_physician=row.get('Primary_Physician'),
            incident_history=row.get('Incident_History')
        )
        db.session.add(patient)
    db.session.commit()
    print("Patients loaded successfully!")

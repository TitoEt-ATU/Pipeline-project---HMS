#!/usr/bin/env python3
"""
Load patient data from CSV into the database.
Usage: python load_patient_data.py
"""
import csv
from datetime import datetime
from src.app import create_app
from src.extensions import db
from src.models import Patient

def load_patients_from_csv(csv_file='patient_records_500_full_history.csv'):
    """Load patient records from CSV file."""
    app = create_app()
    
    with app.app_context():
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            errors = 0
            
            for row in reader:
                try:
                    # Parse date fields
                    dob = None
                    if row.get('Date_of_Birth'):
                        try:
                            dob = datetime.strptime(row['Date_of_Birth'], '%Y-%m-%d').date()
                        except Exception:
                            pass
                    
                    next_appt = None
                    if row.get('Next_Appointment'):
                        try:
                            next_appt = datetime.strptime(row['Next_Appointment'], '%Y-%m-%d').date()
                        except Exception:
                            pass
                    
                    # Create patient
                    patient = Patient(
                        first_name=row.get('First_Name', ''),
                        last_name=row.get('Last_Name', ''),
                        date_of_birth=dob,
                        gender=row.get('Gender', '').strip() or None,
                        blood_type=row.get('Blood_Type', '').strip() or None,
                        phone=row.get('Phone', '').strip() or None,
                        email=row.get('Email', '').strip() or None,
                        address=row.get('Address', '').strip() or None,
                        emergency_contact=row.get('Emergency_Contact_Name', '').strip() or None,
                        emergency_contact_phone=row.get('Emergency_Contact_Phone', '').strip() or None,
                        insurance_provider=row.get('Insurance_Provider', '').strip() or None,
                        insurance_number=row.get('Insurance_Number', '').strip() or None,
                        allergies=row.get('Allergies', '').strip() or None,
                        drug_interactions=row.get('Drug_Interactions', '').strip() or None,
                        past_medical_history=row.get('Past_Medical_History', '').strip() or None,
                        surgical_history=row.get('Surgical_History', '').strip() or None,
                        family_medical_history=row.get('Family_Medical_History', '').strip() or None,
                        social_history=row.get('Social_History', '').strip() or None,
                        immunizations=row.get('Immunizations', '').strip() or None,
                        hospital_stays=row.get('Hospital_Stays', '').strip() or None,
                        next_appointment=next_appt,
                        primary_physician=row.get('Primary_Physician', '').strip() or None,
                        incident_history=row.get('Incident_History', '').strip() or None
                    )
                    
                    db.session.add(patient)
                    count += 1
                    
                    # Commit every 50 records for performance
                    if count % 50 == 0:
                        db.session.commit()
                        print(f"Loaded {count} patients...")
                        
                except Exception as e:
                    errors += 1
                    print(f"Error loading row: {e}")
                    continue
            
            # Final commit
            if count % 50 != 0:
                db.session.commit()
            
            print(f"\n✓ Successfully loaded {count} patients!")
            if errors:
                print(f"⚠ {errors} errors occurred during import")

if __name__ == '__main__':
    load_patients_from_csv()

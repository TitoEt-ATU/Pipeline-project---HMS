from src.extensions import db

# Import only models that exist in this project. Some model files (staff, admin, billing, etc.)
# may be missing in this workspace; import the core ones to avoid import errors.
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.appointment import Appointment
from src.models.medical_record import MedicalRecord
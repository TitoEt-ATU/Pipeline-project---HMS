import sys
import os
import pytest
from datetime import datetime

# Ensure project root is importable so `src` package resolves when running pytest
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.app import create_app
from src.extensions import db
from src.models import Patient, Doctor, MedicalRecord


@pytest.fixture
def app():
    app = create_app()
    # Use an in-memory database for tests to keep them isolated and fast
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()

    yield app

    # teardown inside a fresh app context
    with app.app_context():
        try:
            db.session.remove()
        except Exception:
            pass


def test_medical_records_page_shows_records(app):
    client = app.test_client()

    # prepare test data
    with app.app_context():
        # create a patient (date_of_birth is required)
        p = Patient(first_name='Test', last_name='User', date_of_birth=datetime(1990, 1, 1).date())
        d = Doctor(first_name='Doc', last_name='Tor', specialization='General')
        db.session.add_all([p, d])
        db.session.commit()

        mr = MedicalRecord(patient_id=p.id, doctor_id=d.id, diagnosis='Unit test diagnosis', treatment='None')
        db.session.add(mr)
        db.session.commit()

    resp = client.get('/medical_records')
    assert resp.status_code == 200
    body = resp.data.decode('utf-8')
    assert 'Test User' in body
    assert 'Unit test diagnosis' in body

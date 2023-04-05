import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *
from forms import *

##########This class represents the Medapp test case##########
class MedappTestCase(unittest.TestCase):

###########Define test variables and initialize app.################
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        #self.database_name = "medapp"
        #self.database_path = "postgresql://{}/{}".format('gourikulkarni', 'Kumar18!', 'localhost:5432', self.database_name)
        #setup_db(self.app, self.database_path)

        
##########Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
##########Executed after reach test#######    
    def tearDown(self):
        pass

###########Tests for doctors successful operation and for expected errors.
  
    def test_get_doctors(self):
        response = self.app.get('/doctors')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json())
        self.assertTrue(len(response.get_json()) > 0)
        

    def test_create_doctor_success(self):
        # simulate a GET request to the form for creating a new doctor
        response = self.app.get('/doctors/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        
    def test_create_doctor_error(self):
        # simulate a POST request to create a new doctor without providing the required data
        response = self.app.post('/doctors/create')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing data', response.data)

    def test_get_doctor_edit_page_success(self):
        response = self.app.get(f'/doctors/{self.test_doctor_id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        #self.assertIn(f'value="{self.test_doctor_id}"'.encode(), response.data)
    
    def test_get_doctor_edit_page_error(self):
        # simulate a GET request to edit a non-existent doctor
        response = self.app.get('/doctors/99999/edit')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)
        

    def test_to_delete_doctor(self):
        response = self.app.delete(f'/doctors/delete/{self.test_doctor_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        

    def test_doctor_not_found_to_delete(self):
        response = self.app.get('/doctors/delete/99999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)

###########Tests for patient successful operation and for expected errors.
  
    def test_get_patients(self):
        response = self.app.get('/patients')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json())
        self.assertTrue(len(response.get_json()) > 0)
        

    def test_create_patient_success(self):
        # simulate a GET request to the form for creating a new patient
        response = self.app.get('/patients/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        
    def test_create_patient_error(self):
        # simulate a POST request to create a new patient without providing the required data
        response = self.app.post('/patients/create')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing data', response.data)

    def test_get_patient_edit_page_success(self):
        response = self.app.get(f'/patients/{self.test_patient_id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        
    
    def test_get_patient_edit_page_error(self):
        # simulate a GET request to edit a non-existent patient
        response = self.app.get('/patients/99999/edit')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)
        

    def test_to_delete_patient(self):
        response = self.app.delete(f'/patients/delete/{self.test_patient_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        

    def test_patient_not_found_to_delete(self):
        response = self.app.get('/patients/delete/99999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)

###########Tests for appointment successful operation and for expected errors.
  
    def test_get_appointments(self):
        response = self.app.get('/appointments')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json())
        self.assertTrue(len(response.get_json()) > 0)
        

    def test_create_appointment_success(self):
        # simulate a GET request to the form for creating a new appointment
        response = self.app.get('/appointments/create')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        
    def test_create_appointment_error(self):
        # simulate a POST request to create a new appointment without providing the required data
        response = self.app.post('/appointments/create')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'missing data', response.data)

    def test_get_appointment_edit_page_success(self):
        response = self.app.get(f'/appointments/{self.test_appointment_id}/edit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        
    
    def test_get_appointment_edit_page_error(self):
        # simulate a GET request to edit a non-existent appointment
        response = self.app.get('/appointments/99999/edit')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)
        

    def test_to_delete_appointment(self):
        response = self.app.delete(f'/appointments/delete/{self.test_appointment_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)
        

    def test_appointment_not_found_to_delete(self):
        response = self.app.get('/appointments/delete/99999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'not found', response.data)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
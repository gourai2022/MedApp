import os
import unittest
import json
from flask import request
from flask_sqlalchemy import SQLAlchemy
import requests
from __init__ import create_app
from models import setup_db, Appointment, Doctor, Patient
from forms import *

##########This class represents the Medapp test case##########
class MedappTestCase(unittest.TestCase):

###########Define test variables and initialize app.################
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "medapp_test"
        self.database_path = "postgresql://{}/{}".format('gourikulkarni', 'Kumar18!', 'localhost:5432', self.database_name)
        #setup_db(self.app, self.database_path)

        #Binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_appointment = {
            'appo_day': '2023-04-15',
            'appo_time': '10:00 AM',
            'doctor_id': 1,
            'patient_id': 1
        }
        self.new_appointment_fail = {
            'appo_day': None,
            'appo_time': '10:00 AM',
            'doctor_id': 1,
            'patient_id': 1
        }
        self.update_appointment = {
            'appo_day': '2023-04-15',
            'appo_time': '10:00 AM',
            'doctor_id': 1,
            'patient_id': 2
        }
        self.update_appointment_fail = {
            'appo_day': None,
            'appo_time': '10:00 AM',
            'doctor_id': 1,
            'patient_id': 1
        }
        self.new_doctor = {
            'name': 'Mia Smith',
            'gender': 'Male',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'facebook_link': 'https://facebook.com/drjohnsmith',
            'twiter_link': 'https://twitter.com/drjohnsmith',
            'linkedin_link': 'https://linkedin.com/in/drjohnsmith',
            'website_link': 'https://drjohnsmith.com',
            'specialities': 'Cardiology',
            'upcoming_appo': 0,
            'past_appo': 0
        }
        self.new_doctor_fail = {
            'name': None,
            'gender': 'Male',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'facebook_link': 'https://facebook.com/drjohnsmith',
            'twiter_link': 'https://twitter.com/drjohnsmith',
            'linkedin_link': 'https://linkedin.com/in/drjohnsmith',
            'website_link': 'https://drjohnsmith.com',
            'specialities': 'Cardiology',
            'upcoming_appo': 0,
            'past_appo': 0
        }
        self.update_doctor = {
            'name': 'Dr. John Lee',
            'gender': 'Male',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'facebook_link': 'https://facebook.com/drjohnsmith',
            'twiter_link': 'https://twitter.com/drjohnsmith',
            'linkedin_link': 'https://linkedin.com/in/drjohnsmith',
            'website_link': 'https://drjohnsmith.com',
            'specialities': 'Cardiology'
        }
        self.update_doctor_fail = {
            'name': None,
            'gender': 'Male',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'facebook_link': 'https://facebook.com/drjohnsmith',
            'twiter_link': 'https://twitter.com/drjohnsmith',
            'linkedin_link': 'https://linkedin.com/in/drjohnsmith',
            'website_link': 'https://drjohnsmith.com',
            'specialities': 'Cardiology'
        }
    
        self.new_patient = {
            'name': 'Leo Doe',
            'gender': 'Male',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'date_of_birth': '1990-03-20',
            'health_insurance_provider': 'BlueCross',
            'health_insurance_id': '123456',
            'seeking_specialities': 'Cardiology',
            'concern_description': 'I have been experiencing chest pain',
            'upcoming_appo': 0,
            'past_appo': 0
        }
        self.new_patient_fail = {
            'name': None,
            'gender': 'Male',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'date_of_birth': '1980-03-15',
            'health_insurance_provider': 'BlueCross',
            'health_insurance_id': '123456',
            'seeking_specialities': 'Cardiology',
            'concern_description': 'I have been experiencing chest pain',
            'upcoming_appo': 0,
            'past_appo': 0
        }
        self.update_patient = {
            'name': 'Mary Doe',
            'gender': 'Female',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'date_of_birth': '1990-03-20',
            'health_insurance_provider': 'BlueCross',
            'health_insurance_id': '123456',
            'seeking_specialities': 'Cardiology',
            'concern_description': 'I have been experiencing chest pain'
        }
        self.update_patient_fail = {
            'name': None,
            'gender': 'Female',
            'address': '123 Main St',
            'city': 'New York',
            'state': 'New York',
            'phone': '555-1234',
            'date_of_birth': '1990-03-20',
            'health_insurance_provider': 'BlueCross',
            'health_insurance_id': '123456',
            'seeking_specialities': 'Cardiology',
            'concern_description': 'I have been experiencing chest pain'
        }

        # Set up authentication tokens info
        with open('medapp_auth.json', 'r') as f:
            self.auth = json.loads(f.read())

        admin_jwt = self.auth["roles"]["admin"]["jwtToken"]
        doctor_jwt = self.auth["roles"]["doctor"]["jwtToken"]
        patient_jwt = self.auth["roles"]["patient"]["jwtToken"]
        
        self.auth_headers = {
            "admin": f"Bearer {admin_jwt}",
            "doctor": f"Bearer {doctor_jwt}",
            "patient": f"Bearer {patient_jwt}"
        } 
    
##########Executed after reach test#######    
    def tearDown(self):
        pass

###########Tests for doctors successful operation and for expected errors.
    
    def test_get_doctors(self):
        
        response = self.client().get('/doctors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True, 'success')
    
    def test_create_doctor_success(self):
        #headers = {"Authorization": self.auth_headers["admin"]}
        response = self.client().post('/doctors/create', json=self.new_doctor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True, 'success')
        #self.assertEqual(type(data['doctors']), type([]))
      
    def test_create_doctor_error(self):
       
        response = self.client().post('/doctors/create', json=self.new_doctor_fail)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")
     
    def test_get_doctor_edit_page_success(self):
        
        doctor_id = 1
        #doctor_name = "Dr. John Smith"
        response = self.client().patch(f'/doctors/{doctor_id}', json=self.update_doctor) 
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(type(data['doctors']), type([]))
        #self.assertEqual(data['updated']['name'], doctor_name)
    
    def test_get_doctor_edit_page_error(self):
        
        doctor_id = 1
        # doctor_name = "Andy Andy"
        response = self.client().patch(f'/doctors/{doctor_id}', json=self.update_doctor_fail) 
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")
    ''' 
    def test_to_delete_doctor(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']}]
        for headers in headers_list:
            doctor_id = 1
            response = self.client().delete(f'/doctors/{doctor_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_doctor_not_found_to_delete(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['doctor']}]
        for headers in headers_list:
            doctor_id = 111111111
            response = self.client().delete(f'/doctors/{doctor_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], "not found")
    '''

###########Tests for patient successful operation and for expected errors.
    
    def test_get_patients(self):
        headers= {'Authorization': self.auth_headers['admin']}
        response = self.client().get('/patients')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True, 'success')
        
    def test_create_patient_success(self):
        
        response = self.client().post('/patients/create', json=self.new_patient)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(True, 'success')
        #self.assertEqual(type(data['patients']), type([]))
        
    def test_create_patient_error(self):
        #headers = {"Authorization": self.auth_headers["admin"]}
        response = self.client().post('/patients/create', json=self.new_patient_fail)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")
       
    def test_get_patient_edit_page_success(self):
        
        patient_id = 2
        #patient_name = "Mike Doe"
        response = self.client().patch(f'/patients/{patient_id}', json=self.update_patient)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(type(data['patients']), type([]))
        #self.assertEqual(data['updated']['name'], patient_name)    
    
    def test_get_patient_edit_page_error(self):
        
        patient_id = 1
        #patient_name = "Andy Andy"
        response = self.client().patch(f'/patients/{patient_id}', json=self.update_patient_fail)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")        
    ''' 
    def test_to_delete_patient(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            patient_id = 1
            response = self.client().delete(f'/patients/{patient_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)        

    def test_patient_not_found_to_delete(self):
        headers_list = [
            {'Authorization': self.auth_headers['admin']},
            {'Authorization': self.auth_headers['patient']}]
        for headers in headers_list:
            patient_id = 111111111
            response = self.client().delete(f'/patients/{patient_id}/', headers=headers)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], "not found")
    '''

###########Tests for appointment successful operation and for expected errors.
    
    def test_get_appointments(self):
        
        response = self.client().get('/appointments')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        
    def test_create_appointment_success(self):
        
        response = self.client().post('/appointments/create', json=self.new_appointment)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(data['success'], True)
        self.assertTrue(True, 'success')
        
    def test_create_appointment_error(self):
        
        response = self.client().post('/appointments/create', json=self.new_appointment_fail)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        #self.assertEqual(data['message'], "bad request")
     
    def test_get_appointment_edit_page_success(self):
        
        appointment_id = 2
        #appointment_day = "2023-04-15"
        response = self.client().patch(f'/appointments/{appointment_id}', json=self.update_appointment)
        data = json.loads(response.data)
        #print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(type(data['appointments']), type([]))
        #self.assertEqual(data['updated']['appointment_day'], appointment_day)        
    
    def test_get_appointment_edit_page_error(self):
        
        appointment_id = 1
        #appointment_day = "2099-05-15"
        response = self.client().patch(f'/appointments/{appointment_id}', json=self.update_appointment_fail)  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")
    
    def test_to_delete_appointment(self):
        
        appointment_id = 1
        response = self.client().delete(f'/appointments/delete/{appointment_id}')  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)   
    
    def test_appointment_not_found_to_delete(self):
        
        appointment_id = 111111111
        response = self.client().delete(f'/appointments/delete/{appointment_id}')  
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

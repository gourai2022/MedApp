import os
import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from datetime import date, datetime
from models import setup_db, Appointment, Doctor, Patient

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)
    todat_date = date.today().strftime('%Y-%m-%d')
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type,Authorization,true'
            )
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS'
            )
        return response
    
    ## GET DATA #############################################################################################
    
    @app.route("/doctors")
    @requires_auth("get:doctors")
    def doctors(payload):
        doctors = Doctor.query.all()
        if doctors != None:
            for doctor in doctors:
                    return jsonify({
                                "success": True,
                                "id" : doctor.id,
                                "name": doctor.name,
                            })
        else:
            abort(404, 'not found')
      
    @app.route("/patients")
    @requires_auth("get:patients")
    def patients(payload):
        patients = Patient.query.all()
        if patients != None:
            for patient in patients:
                    return jsonify({
                                "success": True,
                                "id" : patient.id,
                                "name": patient.name,
                            })
        else:    
            abort(404, 'not found')
      
    @app.route("/appointments")
    @requires_auth("get:appointments")
    def appointments(payload):
        appointments = Appointment.query.all()
        if patients != None:
            for appointment in appointments:
                    return jsonify({
                                "success": True,
                                "id" : appointment.id,
                                "appo_day": appointment.appo_day,
                                "appo_time": appointment.appo_time,
                            })
        else:
            abort(404, 'not found')  
      
    ## RECORD DETAILS #############################################################################################  

    @app.route('/doctors/<int:doctor_id>')
    @requires_auth("get:doctor_details")
    def doctor_details(payload, doctor_id):
        try:
            past_appointment_query = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.appo_day < todat_date).order_by(Appointment.appo_day).all()
            upcoming_appointment_query = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.appo_day > todat_date).order_by(Appointment.appo_day).all()
            doctor = Doctor.query.get(Doctor.id == doctor_id)
            if doctor != None:
                return jsonify({
                            "success": True,
                            "id": doctor_id,
                            "name": doctor.name,
                            "gender": doctor.gender,
                            "address": doctor.address,
                            "city": doctor.city,
                            "state": doctor.state,
                            "phone": doctor.phone,
                            "facebook_link": doctor.facebook_link,
                            "twiter_link": doctor.twiter_link,
                            "linkedin_link": doctor.linkedin_link,
                            "website_link": doctor.website_link,
                            "specialities": doctor.specialities,
                            "past_appo": len(past_appointment_query),
                            "upcoming_appo": len(upcoming_appointment_query)
                        })
        except Exception as e:
            print(f'Exception "{e}" in doctor_details()')
            abort(400)      
        
    @app.route('/patients/<int:patient_id>')
    @requires_auth("get:patient_details")
    def patient_details(payload, patient_id):
        try:
            past_appointment_query = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.appo_day < todat_date).order_by(Appointment.appo_day).all()
            upcoming_appointment_query = Appointment.query.filter(Appointment.patient_id == patient_id, Appointment.appo_day > todat_date).order_by(Appointment.appo_day).all()
            patient = Patient.query.get(Patient.id == patient_id)
            if patient != None:
                return jsonify({
                            "success": True,
                            "id": patient_id,
                            "name": patient.name,
                            "gender": patient.gender, 
                            "address": patient.address,
                            "city": patient.city,
                            "state": patient.state,
                            "phone": patient.phone,
                            "date_of_birth": patient.date_of_birth,
                            "health_insurance_provider":patient.health_insurance_provider,
                            "health_insurance_id": patient.health_insurance_id,
                            "seeking_specialities": patient.seeking_specialities,
                            "concern_description":patient.concern_description,
                            "past_appo": len(past_appointment_query),
                            "upcoming_appo": len(upcoming_appointment_query)
                        })
        except Exception as e:
            print(f'Exception "{e}" in patient_details()')
            abort(400)    

    @app.route('/appointments/<int:appointment_id>')
    @requires_auth("get:appointment_details")
    def appointment_details(payload, appointment_id):
        try:
            appointment = Appointment.query.get(Appointment.id == appointment_id)    
            if appointment != None:
                return jsonify({
                            "success": True,
                            "id": appointment_id,
                            "doctor_id": appointment.doctor_id,
                            "patient_id": appointment.patient_id,
                            "appo_day": appointment.appo_day,
                            "appo_time": appointment.appo_time
                        })
        except Exception as e:
            print(f'Exception "{e}" in appointment_details()')
            abort(400)    

    ## CREATE RECORD #############################################################################################  

    @app.route('/doctors/create', methods=['POST'])
    @requires_auth("post:create_doctor")
    def create_doctor(payload):    
        new_doctor = Doctor()
        body = request.get_json()

        new_doctor.name = body.get('name')
        new_doctor.address =body.get('address')
        new_doctor.gender = body.get('gender')
        new_doctor.city = body.get('city')
        new_doctor.state = body.get('state')
        phone = body.get('phone')
        new_doctor.phone = re.sub('\D', '', phone) 
        new_doctor.facebook_link = body.get('facebook_link').strip()
        new_doctor.twiter_link = body.get('twiter_link').strip()
        new_doctor.linkedin_link = body.get('linkedin_link').strip()
        new_doctor.website_link = body.get('website_link').strip()
        new_doctor.specialities = body.get('specialities') 
        new_doctor.upcoming_appo = 0
        new_doctor.past_appo = 0
    
        try:
            if new_doctor.name is None or new_doctor.address is None or new_doctor.gender is None or new_doctor.city is None or new_doctor.state is None or new_doctor.phone is None:
                abort(400, "bad request")
            else:    
                new_doctor.insert()
                return jsonify({
                        "success": True,
                        "id": new_doctor.id,
                        "name": new_doctor.name,
                })
        except Exception as e:
            abort(400, "bad request")

    @app.route('/patients/create', methods=['POST'])
    @requires_auth("post:create_patient")
    def create_patient(payload):    
        new_patient = Patient()
        body = request.get_json()

        new_patient.name = body.get('name')
        new_patient.gender = body.get('gender')
        new_patient.address = body.get('address')
        new_patient.city = body.get('city')
        new_patient.state = body.get('state')
        phone1 = body.get('phone')
        new_patient.phone = re.sub('\D', '', phone1) 
        new_patient.date_of_birth = body.get('date_of_birth')
        new_patient.health_insurance_provider =body.get('health_insurance_provider').strip()
        new_patient.health_insurance_id =body.get('health_insurance_id')
        new_patient.seeking_specialities = body.get('seeking_specialities')
        new_patient.concern_description = body.get('concern_description') 
        new_patient.upcoming_appo = 0
        new_patient.past_appo = 0
        try:
            if new_patient.name is None or new_patient.address is None or new_patient.gender is None or new_patient.city is None or new_patient.state is None or new_patient.phone is None or new_patient.date_of_birth is None or new_patient.health_insurance_provider is None or new_patient.health_insurance_id is None or new_patient.seeking_specialities is None:
                abort(400, "bad request")
            else:    
                new_patient.insert()
                return jsonify({
                        "success": True,
                        "id": new_patient.id,
                        "name": new_patient.name,
                })
        except Exception as e:
            abort(400, "bad request")

    @app.route('/appointments/create', methods=['POST'])
    @requires_auth("post:create_appointment")
    def create_appointment(payload):
        new_appointment = Appointment()
        body = request.get_json()
        new_appointment.patient_id = body.get('patient_id')
        new_appointment.doctor_id = body.get('doctor_id')
        new_appointment.appo_day = body.get('appo_day')
        new_appointment.appo_time = body.get('appo_time')
        appointment_time = new_appointment.appo_time
        try:
            if new_appointment.appo_day is None or new_appointment.appo_time is None or new_appointment.doctor_id is None or new_appointment.patient_id is None:
                abort(400, "bad request")
            else:  
                #new_appointment = Appointment(appo_day=appo_day, appo_time=appo_time, doctor_id=doctor_id, patient_id=patient_id )
                new_appointment.insert()
                '''
                updated_patient = Patient.query.get(patient_id)
                updated_doctor = Doctor.query.get(doctor_id)
                if updated_patient != None and updated_doctor != None:
                    if appointment_time < date.today().strftime('%Y-%m-%d'):
                        doctor_upcoming_appo = int(updated_doctor.upcoming_appo + 1)
                        patient_upcoming_appo = int(updated_patient.upcoming_appo + 1) 
                        
                    elif appointment_time > date.today().strftime('%Y-%m-%d'):
                        doctor_past_appo = int(updated_doctor.past_appo + 1)
                        patient_past_appo = int(updated_patient.past_appo + 1)
                        
                updated_doctor = Doctor(upcoming_appo=doctor_upcoming_appo , past_appo=doctor_past_appo)
                updated_patient = Patient(upcoming_appo=patient_upcoming_appo , past_appo=patient_past_appo)
                updated_patient.merge()
                updated_doctor.merge()
                '''
                return jsonify({
                        "success": True,
                        "id": new_appointment.id,
                        "appo_day": new_appointment.appo_day,
                })
        except Exception as e:
            abort(400, "bad request")

    ## UPDATE RECORD #############################################################################################  

    @app.route('/doctors/<int:doctor_id>', methods=['PATCH'])
    @requires_auth("patch:edit_doctor")
    def update_doctor(payload, doctor_id):   
        body = request.get_json()
        update_doctor = Doctor.query.get(doctor_id)
        try:
            if update_doctor: 
                update_doctor.name = body.get('name')
                update_doctor.gender =  body.get('gender')
                update_doctor.address =  request.json.get('address')
                update_doctor.city = body.get('city')
                update_doctor.state =  body.get('state')
                update_doctor.phone =  body.get('phone')
                update_doctor.facebook_link =  body.get('facebook_link').strip()
                update_doctor.twiter_link =  body.get('twiter_link').strip()
                update_doctor.linkedin_link =  body.get('linkedin_link').strip()
                update_doctor.website_link =  body.get('website_link').strip()
                update_doctor.specialities =  body.get('specialities') 
                #update_doctor.upcoming_appo = 0
                #update_doctor.past_appo = 0
                
                if update_doctor.name is None or update_doctor.address is None or update_doctor.gender is None or update_doctor.city is None or update_doctor.state is None or update_doctor.phone is None:
                    abort(404, "not found")
                else:
                    update_doctor.update()
                    return jsonify({
                        "success": True,
                        "updated": update_doctor.format()
                    })
        except Exception as e:
            abort(404, "not found")
    
    @app.route('/patients/<int:patient_id>', methods=['PATCH'])
    @requires_auth("patch:edit_patient")
    def update_patient(payload, patient_id):
        body = request.get_json()
        update_patient = Patient.query.get(patient_id)
        try:
            if update_patient: 
                update_patient.name = body.get('name')
                update_patient.gender = body.get('gender')
                update_patient.address = body.get('address')
                update_patient.city = body.get('city')
                update_patient.state = body.get('state')
                update_patient.phone = body.get('phone')
                update_patient.date_of_birth = body.get('date_of_birth')
                update_patient.health_insurance_provider =body.get('health_insurance_provider').strip()
                update_patient.health_insurance_id =body.get('health_insurance_id')
                update_patient.seeking_specialities = body.get('seeking_specialities')
                update_patient.concern_description = body.get('concern_description') 
                
                if update_patient.name is None or update_patient.address is None or update_patient.gender is None or update_patient.city is None or update_patient.state is None or update_patient.phone is None or update_patient.date_of_birth is None or update_patient.health_insurance_provider is None or update_patient.health_insurance_id is None or update_patient.seeking_specialities is None:
                    abort(404, "not found")
                else:
                    update_patient.update()
                    return jsonify({
                        "success": True,
                        "updated": update_patient.format()
                    })
        except Exception as e:
            abort(404, "not found")    

    @app.route('/appointments/<int:appointment_id>', methods=['PATCH'])
    @requires_auth("patch:edit_appointment")
    def update_appointment(payload, appointment_id):
        body = request.get_json()
        update_appointment = Appointment.query.get(appointment_id)
        try:
            if update_appointment: 
                update_appointment.appo_day =  body.get('appo_day')
                update_appointment.appo_time = body.get('appo_time')
                #update_appointment.appo_available = body.get('appo_available')
                update_appointment.doctor_id = body.get('doctor_id')
                update_appointment.patient_id = body.get('patient_id')
                
                if update_appointment.appo_day is None or update_appointment.appo_time is None or update_appointment.doctor_id is None or update_appointment.patient_id is None:
                    abort(404, "not found")
                else:
                    update_appointment.update()
                    return jsonify({
                            "success": True,
                            "updated": update_appointment.format()
                        })
        except Exception as e:
            abort(404, "not found")
            
    
    ## DELETE RECORD #############################################################################################  
    
    @app.route('/appointments/delete/<int:appointment_id>', methods=['DELETE'])
    @requires_auth("delete:appointment")
    def delete_appointment(payload, appointment_id):
        delete_appointment = Appointment.query.filter(Appointment.id == appointment_id).first()
        #updated_patient = Patient.query.get(delete_appointment.patient_id)
        #updated_doctor = Doctor.query.get(delete_appointment.doctor_id)
        try:
            if delete_appointment is None:
                abort(404, "not found")
            else:    
                '''
                if delete_appointment.appo_day < date.today().strftime("%Y/%m/%d"):
                    updated_patient.upcoming_appo = int(updated_patient.upcoming_appo - 1) 
                    updated_doctor.upcoming_appo = int(updated_doctor.upcoming_appo - 1)

                elif delete_appointment.appo_day > date.today().strftime("%Y/%m/%d"):
                    updated_patient.past_appo = int(updated_patient.past_appo - 1)
                    updated_doctor.past_appo = int(updated_doctor.past_appo - 1)
                '''
                delete_appointment.delete()
                return jsonify({
                    "success": True,
                    "deleted": appointment_id
                })
        
        except Exception as e:
            abort(404, "not found")
    
    #########################################DONE##########################################################################

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}), 
            400,
        )

    @app.errorhandler(404)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 404, "message": "not found"}), 
            404,
        )

    @app.errorhandler(405)
    def invalid_method(error):
        return (
            jsonify({"success": False, "error": 405, "message": "invalid method"}), 
            405,
        )

    @app.errorhandler(422)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 422, "message": "Unprocessable recource"}), 
            422,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}), 
            500,
        )  
    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({"success": False, "error": auth_error.status_code, "message": auth_error.error['description']}), auth_error.status_code  

    return app
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

app = create_app()

if __name__ == '__main__':
    app.run()
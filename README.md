MEDAPP

Introduction

Medapp is a medical appointment booking API that facilitates to  booking appointment to specific doctor for specific doctors speciality. This API lets you list new patient and doctors, discover them.

Here I build the data models to power the API endpoints for the Medapp site by connecting to a PostgreSQL database for storing, querying, and creating information about patient and doctor and appointments on Medapp.

Overview

This is a medical appointment booking app that allows patients to book appointments with doctors. The app has create, display, update, and delete functionality for patients, doctors, and appointments in JSONIFY format.

Features —
Patients can create a new account
Patients can view their appointment history and upcoming appointments
Patients can view a doctor's profile and availability
Patients can cancel appointments they have booked
Doctors can create a new account
Doctors can update their availability for appointments
Doctors can cancel appointments that they have booked
Admins can create a new account
Admins can view all patients, doctors, and appointments
Admins can add, edit, or delete patients, doctors, or appointments

Tech Stack (Dependencies)

1. Backend Dependencies
Our tech stack will include the following:
 — virtualenv** as a tool to create isolated Python environments
 — SQLAlchemy ORM** to be our ORM library of choice
 — PostgreSQL** as our database of choice
 — Python3** and **Flask** as our server language and server framework
 — Flask-Migrate** for creating and running schema migrations
You can download and install the dependencies mentioned above using 

`pip` as:
```
Pip3 install virtualenv
Pip3 install SQLAlchemy
Pip3 install postgres
Pip3 install Flask
Pip3 install Flask-Migrate
```
**Note** - If we do not mention the specific version of a package, then the default latest stable package will be installed. 

2. Frontend Dependencies
You must have the HTML, CSS, and Javascript with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend. Bootstrap can only be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/). Windows users must run the executable as an Administrator, and restart the computer after installation. After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend:
```
npm init -y
npm install bootstrap@3
```

Main Files: Project Structure

  ├── README.md
  ├── __init__.py *** the main driver of the app. Includes your SQLAlchemy models. "python app.py" to run after installing dependencies
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── manage.py
  ├── models.py 
  ├── test_app.py
  ├── setup.sh
  ├── auth.py
  └── medapp_auth.json
      

API Documentation

Models
There are two models:
*Doctor
*Patient
*Appointment


Error Handling

Errors are returned as JSON objects in the following format:
jsonify
({
"success": False, 
"error": 500, 
"message": "Internal server error”
}),500


Endpoints

GET - /doctors
      /patients
      /appointmets

POST - /doctor/create
       /patient/create       
       /appointment/create

PATCH - /doctor/doctor_id 
        /patient/patient_id
        /appointment/appointment_id

DELETE - /doctor/delete/doctor_id  #### Disabled for user restiction 
         /patient/delete/patient_id #### Disabled for user restiction
         /appointment/delete/appointment_id       



Auth0 Setup

You need to setup an Auth0 account.
Environment variables needed: (setup.sh)

export AUTH0_DOMAIN="---------.auth0.com" # Choose your tenant domain
export ALGORITHMS="RS256"
export API_AUDIENCE="MedApp" # Create an API in Auth0

To run the tests, run

dropdb medapp_test
createdb medapp_test
psql medapp_test < medapp.psql
python3 test_app.py
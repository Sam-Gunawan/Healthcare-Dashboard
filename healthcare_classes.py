"""The collection of class definitions for the healthcare management system"""
from datetime import date
import streamlit as st
import pandas as pd
import random as rand

PATIENTS_FILE = "./dataset/patients.csv"
DOCTORS_FILE = "./dataset/doctors.csv"
APPOINTMENTS_FILE = "./dataset/appointments.csv"
PATIENT_MEDICAL_HISTORY_FILE = "./dataset/patient_medical_history.csv"
APPOINTMENT_ASSIGNMENT_FILE = "./dataset/patient_appointment_doctor.csv"

class Person:
    def __init__(self, name: str, gender: str = "", email: str = "", date_of_birth: str = "", phone_number: int = ""):
        self.name = name
        self.gender = gender
        self.email = email
        self.date_of_birth = date_of_birth
        self.phone_number = phone_number
    
    def __str__(self):
        return f"""
Name: {self.name}
Email: {self.email}
Gender: {self.gender}
DOB: {self.date_of_birth}
Phone: {self.phone_number}"""
    
test_person = Person("Evan", "email", "male", "1212")
# print(test_person)

class Appointment:
    def __init__(self, appointment_date: date, status: bool, complaint: str, symptoms: str = "[TBA]", diagnosis: str = "[TBA]", treatment: str = "[TBA]"):
        self.appointment_date = appointment_date
        self.status = status
        self.complaint = complaint
        self.symptoms = symptoms
        self.diagnosis = diagnosis
        self.treatment = treatment 

        self.appointment_df = pd.read_csv("./dataset/appointments.csv", sep=';')
        self.appointment_id = self.generate_id(self.appointment_df)
    
    def generate_id(self, appointment_df: pd.DataFrame):
        # find number of current rows and format it to be "A..." with the current appointment to be [number of rows + 1] incl. leading zeros (3 digits)
        new_index = len(appointment_df) + 1
        return "A" + f"{new_index:03}"

    def __str__(self):
        return f"""Appointment ID: {self.appointment_id}
Date: {self.appointment_date}
Status: {self.status}
Complaints: {self.complaint}
Symptoms: {self.symptoms}
diagnosis: {self.diagnosis}
Treatment: {self.treatment}"""

today = date.today()
test_appointment = Appointment(today, 0, "This is a complaint")
# print(test_appointment)


class Doctor(Person):
    def __init__(self, name: str, doctor_id: str, specialization: str, office: str, email: str = "", gender: str = "", date_of_birth: str = "", phone_number:str = ""):
        super().__init__(name, gender, email, date_of_birth, phone_number)
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.office = office
    
    def complete_appointment(self, appointment_file, appointment_id: str, diagnostic: str, symptoms: str, treatment: str):
        new_medical_record = MedicalRecord(diagnostic, symptoms, treatment)
        df = pd.read_csv(appointment_file, sep=';')
        df.loc[df["Appointment ID"] == appointment_id, "Status"] = "completed"
        df.loc[df["Appointment ID"] == appointment_id, "Diagnostic"] = diagnostic
        df.loc[df["Appointment ID"] == appointment_id, "Symptoms"] = symptoms
        df.loc[df["Appointment ID"] == appointment_id, "Treatment"] = treatment

        st.write(df)
        df.to_csv(appointment_file, sep=';', index=False)

        return new_medical_record

    def __str__(self):
        return f"""
Doctor ID: {self.doctor_id}
Specialization: {self.specialization} {super().__str__()}
Office: {self.office}"""
    
test_doctor = Doctor("Jorel", "email", "male", "0812", 62811, "D001", "Neurology", "Lavenue")
# print(test_doctor)

class MedicalRecord:
    def __init__(self, diagnostic: str, symptoms: str, treatment: str):
        self.diagnostic = diagnostic
        self.symptoms = symptoms
        self.treatment = treatment

    def summary(self):
        return f"""diagnostic: {self.diagnostic}
Symptoms: {self.symptoms}
Treatment: {self.treatment}"""
    
test_med_record = MedicalRecord("COVID-19", "Fever, fatigue", "Prescribed high vitamin D drugs")
test_med_record2 = MedicalRecord("Flu", "Fever, fatigue", "Prescribed high vitamin D drugs")
# print(test_med_record.summary())

class Patient(Person):
    def __init__(self, name: str, email: str, gender: str, date_of_birth: str, phone_number: str, medical_history: list[MedicalRecord]="", patient_id: str = ""):
        super().__init__(name, gender, email, date_of_birth, phone_number)
        self.patient_df = pd.read_csv("./dataset/patients.csv", sep=';')
        self.patient_id = patient_id

        saved_medical_history = self.get_medical_history()
        if saved_medical_history == []:
            self.medical_history = medical_history

    def generate_id(self):
        new_index = len(self.patient_df) + 1
        return "P" + f"{new_index:03}"

    def add_account(self):
        new_id = self.generate_id()
        self.patient_id = new_id
        new_patient = {
            "Patient ID": [self.patient_id],
            "Name": [self.name.title()],
            "Gender": [self.gender],
            "Date of Birth": [self.date_of_birth],
            "Contact": [self.phone_number],
            "Email": [self.email]
        }

        new_patient_df = pd.DataFrame(new_patient)
        new_patient_df.to_csv("./dataset/patients.csv", mode='a', index=False, header=False, sep=';')

        return new_id
    
    def get_medical_history(self):
        medical_history = []
        history_df = pd.read_csv(PATIENT_MEDICAL_HISTORY_FILE, sep=';')
        patient_history = history_df[history_df['patient_id'] == self.patient_id]

        for _, row in patient_history.iterrows():
            record = MedicalRecord(row['medical_history'], "", "")
            medical_history.append(record)

        return medical_history

    def read_medical_history(self):
        readable_history = ""
        
        # if no records exist, replace with message
        if len(self.medical_history) == 0:
            return "No history"
        # if only 1 record exist, just return the medical record instantly
        elif len(self.medical_history) == 1:
            return self.medical_history[0].diagnostic

        for medical_record in self.medical_history[:-1]:
            # concatenate medical records up till the second last record using commas to separate them.
            readable_history += f"{medical_record.diagnostic}, "

        # add the last record without having to add another comma
        readable_history += self.medical_history[-1].diagnostic

        return readable_history
    
    def add_appointment(self, appointment_request: Appointment):
        appointment_id = appointment_request.appointment_id
        date = appointment_request.appointment_date
        status = "pending" if not appointment_request.status else "completed"
        complaint = appointment_request.complaint
        symptoms = appointment_request.symptoms
        diagnostic = appointment_request.diagnosis
        treatment = appointment_request.treatment

        new_appointment = {
            "Appointment ID": [appointment_id],
            "Date": [date],
            "Status": [status],
            "Complaints": [complaint],
            "Symptoms": [symptoms],
            "Diagnostic": [diagnostic],
            "Treatment": [treatment]
        }

        new_appointment_df = pd.DataFrame(new_appointment)
        new_appointment_df.to_csv("./dataset/appointments.csv", mode='a', index=False, header=False, sep=';')

        randomly_assigned_doctor = "D00" + str(rand.randint(1, 6))
        new_assigned_doctor = {
            "patient_id": [self.patient_id],
            "appointment_id": [appointment_id],
            "doctor_id": [randomly_assigned_doctor]
        }

        new_assigned_doctor_df = pd.DataFrame(new_assigned_doctor)
        new_assigned_doctor_df.to_csv("./dataset/patient_appointment_doctor.csv", mode='a', index=False, header=False, sep=';')

    def add_medical_history(self, medical_record: MedicalRecord):
        # Load the medical history CSV
        history_df = pd.read_csv(PATIENT_MEDICAL_HISTORY_FILE, sep=';')

        # Append new record
        new_record = {
            'patient_id': self.patient_id,
            'medical_history': medical_record.diagnostic,
            'Symptoms': medical_record.symptoms,
            'Treatment': medical_record.treatment
        }
        history_df = pd.concat([history_df, pd.DataFrame([new_record])], ignore_index=True)

        # Save the updated file
        history_df.to_csv(PATIENT_MEDICAL_HISTORY_FILE, sep=';', index=False)

    def __str__(self):
        return f"""
Patient ID: {self.patient_id} {super().__str__()}
Medical history: {self.read_medical_history()}"""
    
class AppointmentAssignment:
    def __init__(self, patient: Patient, doctor: Doctor, appointment: Appointment):
        self.patient = patient
        self.doctor = doctor
        self.appointment = appointment
    
    def get_patient_appointment_details(self, patient_id, patients_file, appointments_file, patient_appointments_file, doctors_file):
        # Load all CSV files into DataFrames
        patients_df = pd.read_csv(patients_file, sep=";")
        appointments_df = pd.read_csv(appointments_file, sep=";")
        patient_appointments_df = pd.read_csv(patient_appointments_file, sep=";")
        doctors_df = pd.read_csv(doctors_file, sep=";")
        
        # Filter patient data
        patient_info = patients_df[patients_df['Patient ID'].str.upper() == patient_id.upper()]
        if patient_info.empty:
            return f"No patient found with ID {patient_id}."
        
        # Merge patient_appointments with appointments to get appointment details
        merged_appointments = pd.merge(patient_appointments_df, appointments_df, left_on="appointment_id", right_on="Appointment ID")
        
        # Further merge with doctors to get doctor's name
        merged_data = pd.merge(merged_appointments, doctors_df, left_on="doctor_id", right_on="Doctor ID")
        
        # Filter for the given patient ID
        patient_appointments = merged_data[merged_data['patient_id'].str.upper() == patient_id.upper()]
        
        # Check if any appointments exist for the patient
        if patient_appointments.empty:
            return "empty"
        
        # Extract relevant columns and patient details
        patient_name = patient_info.iloc[0]['Name']
        details = []
        for _, row in patient_appointments.iterrows():
            detail = {
                "Patient Name": patient_name,
                "Appointment ID": row["Appointment ID"],
                "Status": row["Status"].title(),
                "Date": row["Date"],
                "Complaint": row['Complaints'],
                "Diagnosis": row["Diagnostic"] if row["Diagnostic"] != "[TBA]" else "Not Available",
                "Symptoms": row["Symptoms"] if row["Symptoms"] != "[TBA]" else "Not Available",
                "Treatment": row["Treatment"] if row["Treatment"] != "[TBA]" else "Not Available",
                "Doctor Name": row["Name"],
            }
            details.append(detail)

        return details

    def get_doctor_appointment_details(self, doctor_id, patients_file, appointments_file, doctor_appointments_file, doctors_file):
        # load all CSV files into DataFrames
        patients_df = pd.read_csv(patients_file, sep=";")
        appointments_df = pd.read_csv(appointments_file, sep=";")
        doctor_appointments_df = pd.read_csv(doctor_appointments_file, sep=";")
        doctors_df = pd.read_csv(doctors_file, sep=";")
        
        # filter doctor data
        doctor_info = doctors_df[doctors_df['Doctor ID'].str.upper() == doctor_id.upper()]
        if doctor_info.empty:
            return f"No doctor found with ID {doctor_id}."
        
        # merge doctor_appointments with appointments to get appointment details
        merged_appointments = pd.merge(doctor_appointments_df, appointments_df, left_on="appointment_id", right_on="Appointment ID")
        
        # further merge with patients to get patient's name
        merged_data = pd.merge(merged_appointments, patients_df, left_on="patient_id", right_on="Patient ID")
        
        # filter for the given doctor ID
        doctor_appointments = merged_data[merged_data['doctor_id'].str.upper() == doctor_id.upper()]
        
        # check if any appointments exist for the doctor
        if doctor_appointments.empty:
            return "empty"
        
        # extract relevant columns and doctor details
        doctor_name = doctor_info.iloc[0]['Name']
        details = []
        for _, row in doctor_appointments.iterrows():
            detail = {
                "Doctor Name": doctor_name,
                "Patient Name": row["Name"],
                "Appointment ID": row["Appointment ID"],
                "Status": row["Status"].title(),
                "Date": row["Date"],
                "Complaint": row['Complaints'],
                "Diagnosis": row["Diagnostic"] if row["Diagnostic"] != "[TBA]" else "Not Available",
                "Symptoms": row["Symptoms"] if row["Symptoms"] != "[TBA]" else "Not Available",
                "Treatment": row["Treatment"] if row["Treatment"] != "[TBA]" else "Not Available",
            }
            details.append(detail)

        return details
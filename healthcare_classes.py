"""The collection of class definitions for the healthcare management system"""
from datetime import date
import streamlit as st
import pandas as pd
import random as rand

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
    def __init__(self, name: str, email: str, gender: str, date_of_birth: str, phone_number: str, medical_history: list[MedicalRecord], patient_id: str = ""):
        super().__init__(name, gender, email, date_of_birth, phone_number)
        self.medical_history = medical_history

        self.patient_df = pd.read_csv("./dataset/patients.csv", sep=';')
        self.patient_id = patient_id

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

    def reschedule_appointment(self, appointment_id: str, new_date: str):
        pass
        # TODO

    def add_medical_history(self, medical_record: MedicalRecord):
        pass
        # TODO

    def __str__(self):
        return f"""
Patient ID: {self.patient_id} {super().__str__()}
Medical history: {self.read_medical_history()}"""
    
# test_med_history = []
test_med_history = [test_med_record, test_med_record2]

test_patient = Patient("Sam", "email", "male", "0812", 62811, "P001", test_med_history)
# print(test_patient) 

test_new_patient = Patient("Dory", "email", "female", "121212", "1212", [])
# print(test_new_patient.generate_id())
# print(test_new_patient)

"""The collection of class definitions for the healthcare management system"""
from datetime import date
import streamlit as st
import pandas as pd
import random as rand

class Person:
    def __init__(self, name: str, email: str = "", gender: str = "", date_of_birth: str = "", phone_number: int = ""):
        self.name = name
        self.email = email
        self.gender = gender
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
    def __init__(self, appointment_id: str, appointment_date: date, status: bool, complaint: str, symptoms: str = "[TBA]", diagnose: str = "[TBA]", treatment: str = "[TBA]"):
        self.appointment_id = appointment_id
        self.appointment_date = appointment_date
        self.status = status
        self.complaint = complaint
        self.symptoms = symptoms
        self.diagnose = diagnose
        self.treatment = treatment 

class Doctor(Person):
    def __init__(self, name: str, office: str, email: str = "", gender: str = "", date_of_birth: str = "", phone_number:str = "", doctor_id: str = "", specialization: str = ""):
        super().__init__(name, email, gender, date_of_birth, phone_number)
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.office = office
    
    def finish_appointment(self, illness: str, symptoms: str, treatment: str):
        pass
        # TODO

    def __str__(self):
        return f"""
Doctor ID: {self.doctor_id}
Specialization: {self.specialization} {super().__str__()}
Office: {self.office}"""
    
test_doctor = Doctor("Jorel", "email", "male", "0812", 62811, "D001", "Neurology", "Lavenue")
# print(test_doctor)

class MedicalRecord:
    def __init__(self, illness: str, symptoms: str, treatment: str):
        self.illness = illness
        self.symptoms = symptoms
        self.treatment = treatment

    def summary(self):
        return f"""Illness: {self.illness}
Symptoms: {self.symptoms}
Treatment: {self.treatment}"""
    
test_med_record = MedicalRecord("COVID-19", "Fever, fatigue", "Prescribed high vitamin D drugs")
test_med_record2 = MedicalRecord("Flu", "Fever, fatigue", "Prescribed high vitamin D drugs")
# print(test_med_record.summary())

class Patient(Person):
    def __init__(self, name: str, email: str, gender: str, date_of_birth: str, phone_number: str, patient_id: str, medical_history: list[MedicalRecord]):
        super().__init__(name, gender, email, date_of_birth, phone_number)
        self.patient_id = patient_id
        self.medical_history = medical_history

    def read_medical_history(self):
        readable_history = ""
        
        # if no records exist, replace with message
        if len(self.medical_history) == 0:
            return "No history"
        # if only 1 record exist, just return the medical record instantly
        elif len(self.medical_history) == 1:
            return self.medical_history[0].illness

        for medical_record in self.medical_history[:-1]:
            # concatenate medical records up till the second last record using commas to separate them.
            readable_history += f"{medical_record.illness}, "

        # add the last record without having to add another comma
        readable_history += self.medical_history[-1].illness

        return readable_history
    
    def add_appointment(self, appointment_request: Appointment):
        appointment_id = appointment_request.appointment_id
        date = appointment_request.appointment_date
        status = "pending" if not appointment_request.status else "completed"
        complaint = appointment_request.complaint
        symptoms = appointment_request.symptoms
        diagnostic = appointment_request.diagnose
        treatment = appointment_request.treatment

        new_appointment = {
            "Appointment ID": appointment_id,
            "Date": date,
            "Status": status,
            "Complaints": complaint,
            "Symptoms": symptoms,
            "Diagnostic": diagnostic,
            "Treatment": treatment
        }

        new_appointment_df = pd.DataFrame(new_appointment)
        new_appointment_df.to_csv("./dataset/appointments.csv", mode='a', index=False, header=False, sep=';')

        randomly_assigned_doctor = "D00" + str(rand.randint(1, 6))
        new_assigned_doctor = {
            "patient_id": self.patient_id,
            "appointment_id": appointment_id,
            "doctor_id": randomly_assigned_doctor
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

class AppointmentDetail:
    def __init__(self, patient: Patient, appointment_id: str, appointment_date: str, complaint: str):
        self.patient = patient
        self.appointment_id = appointment_id
        self.appointment_date = appointment_date
        self.complaint = complaint

    def set_appointment_date(self, new_date):
        self.appointment_date = new_date
    
    def summary(self):
        return f"""Patient ID: {self.patient.patient_id}
Appointment ID: {self.appointment_id}
Date: {self.appointment_date}
Complaint: {self.complaint}"""
    
test_appointment_detail = AppointmentDetail(test_patient, "A001", "1234", "My head is dizzy")
# print(test_appointment_detail.summary())

class AppointmentResult:
    def __init__(self, doctor: Doctor, appointment_detail: AppointmentDetail, illness: str, symptoms: str, treatment: str):
        self.doctor = doctor
        self.appointment_detail = appointment_detail
        self.illness = illness
        self.symptoms = symptoms
        self.treatment = treatment

    def summary(self):
        return f"""{self.appointment_detail.summary()}
---Results---
Doctor: {self.doctor.doctor_id}
Illness: {self.illness}
Symptoms: {self.symptoms}
Treatment: {self.treatment}"""
    
test_appointment = AppointmentResult(test_doctor, test_appointment_detail, "Diare", "Poop 10x a day", "Diapet")
# print(test_appointment.summary())   

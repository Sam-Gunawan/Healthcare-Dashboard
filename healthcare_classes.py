"""The collection of class definitions for the healthcare management system"""

class Person:
    def __init__(self, name: str, email: str, gender: str, date_of_birth: str, phone_number: int):
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
    
test_person = Person("Evan", "email", "male", "1212", 811)
# print(test_person)

class Doctor(Person):
    def __init__(self, name: str, email: str, gender: str, date_of_birth: str, phone_number:str, doctor_id: str, specialization: str, office: str):
        super().__init__(name, email, gender, date_of_birth, phone_number)
        self.doctor_id = doctor_id
        self.specialization = specialization
        self.office = office

    def __str__(self):
        return f"""
Doctor ID: {self.doctor_id}
Specialization: {self.specialization} {super().__str__()}
Office: {self.office}"""
    
test_doctor = Doctor("Jorel", "email", "male", "0812", 62811, "D001", "Neurology", "Lavenue")
# print(test_doctor)

class Patient(Person):
    def __init__(self, name: str, email: str, gender: str, date_of_birth: str, phone_number:str, patient_id: str, medical_history: list):
        super().__init__(name, gender, email, date_of_birth, phone_number)
        self.patient_id = patient_id
        self.medical_history = medical_history

    def read_medical_history(self):
        readable_history = ""
        
        # if no records exist, replace with message
        if len(self.medical_history) == 0 or self.medical_history[0] == "":
            return "No history"
        # if only 1 record exist, just return the medical record instantly
        elif len(self.medical_history) == 1:
            return self.medical_history[0]

        for medical_record in self.medical_history[:-1]:
            # concatenate medical records up till the second last record using commas to separate them.
            readable_history += f"{medical_record}, "

        # add the last record without having to add another comma
        readable_history += self.medical_history[-1]

        return readable_history

    def __str__(self):
        return f"""
Patient ID: {self.patient_id} {super().__str__()}
Medical history: {self.read_medical_history()}"""
    
test_med_history = ["Flu", "TB", "COVID-19"]
# test_med_history = [""]
# test_med_history = []
# test_med_history = ["Flu"]

test_patient = Patient("Sam", "email", "male", "0812", 62811, "P001", test_med_history)
# print(test_patient)

class MedicalRecord:
    def __init__(self, illness: str, symptoms: str, treatment: str):
        self.illness = illness
        self.symptoms = symptoms
        self.treatment = treatment

    def summary(self):
        return f"""Illness: {self.illness}
Symptoms: {self.symptoms}
Treatment: {self.treatment}"""
    
# TODO: integrate MedicalRecord object to the medical_history attirbute of Patient object.
# test_med_record = MedicalRecord("COVID-19", "Fever, fatigue", "Prescribed high vitamin D drugs")
# print(test_med_record.summary())

class AppointmentDetail:
    def __init__(self, appointment_id: str, appointment_date: str):
        self.appointment_id = appointment_id
        self.appointment_date = appointment_date

    def set_appointment_date(self, new_date):
        self.appointment_date = new_date
    
    def summary(self):
        return f"Appointment ID: {self.appointment_id}\nDate: {self.appointment_date}"
    
test_appointment_detail = AppointmentDetail("A001", "1234")
# print(test_appointment_detail.summary())

class Appointment:
    def __init__(self, patient: Patient, doctor: Doctor, appointment_detail: AppointmentDetail):
        self.patient = patient
        self.doctor = doctor
        self.appointment_detail = appointment_detail
    
    def add_patient_history(self):
        pass
        # this is in the OODB diagram, don't understand what it does
        # TODO: ask Evan what it means and its purpose

    def summary(self):
        return f"""{self.appointment_detail.summary()}
Patient: {self.patient.patient_id}
Doctor: {self.doctor.doctor_id}"""
    
test_appointment = Appointment(test_patient, test_doctor, test_appointment_detail)
# print(test_appointment.summary())
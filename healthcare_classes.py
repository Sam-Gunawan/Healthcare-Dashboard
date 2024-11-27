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
    
# test_person = Person("Sam", "email", "male", "1212", 811)
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
    
# test_doctor = Doctor("Sam", "email", "male", "0812", 62811, "D001", "Neurology", "Lavenue")
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
    
# test_med_history = ["Flu", "TB", "COVID-19"]
# test_med_history = [""]
# test_med_history = []
# test_med_history = ["Flu"]

# test_patient = Patient("Sam", "email", "male", "0812", 62811, "P001", test_med_history)
# print(test_patient)
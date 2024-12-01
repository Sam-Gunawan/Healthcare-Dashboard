import streamlit as st
from healthcare_classes import *
import pandas as pd
import datetime as dt


def sign_up():
    st.title('Welcome to :blue[Health First]')
    patient_name = st.text_input('Name')
    patient_gender = st.selectbox('Gender', ['Male', 'Female'])
    patient_dob = st.date_input('Date of Birth')
    patient_number = st.text_input('Contact Number') 
    patient_email = st.text_input('Email Address')

    if st.button('Create account'):
        if not patient_name:
            st.error("Name is required!")
        elif not patient_gender:
            st.error("Gender is required!")
        elif not patient_number:
            st.error("Contact Number is required!")
        elif not patient_email:
            st.error("Email Address is required!")
        else:
            # TODO: all checks valid, add patient to database
            st.session_state.current_page = "request_appointment"

    return patient_name, patient_gender, patient_dob, patient_number, patient_email

def run_patient_dashboard(patient_id):
    # search for patient data in dataframe
    patient_data = df[(df['Patient ID'].str.upper() == patient_id.upper())].values
    
    patient_id = patient_data[0][0]
    patient_name = patient_data[0][1]
    patient_gender = patient_data[0][2]
    patient_dob = patient_data[0][3]
    patient_number = patient_data[0][4]
    patient_email = patient_data[0][5]

    current_patient = Patient(patient_name, patient_email, patient_gender, patient_dob, patient_number, patient_id, [""]) # TODO: implement medical history

    st.subheader("Profile")
    st.write("Patient ID: ", patient_id)
    st.write("Name: ", patient_name)
    st.write("Gender: ", patient_gender)
    st.write("DOB: ", patient_dob)
    st.write("Contact: ", patient_number)
    st.write("Email: ", patient_email)

    st.divider()
    st.subheader("My Appointments")
    appointments = get_patient_appointment_details(patient_id, "./dataset/patients.csv", "./dataset/appointments.csv", "./dataset/patient_appointment_doctor.csv", "./dataset/doctors.csv")
    for appointment in appointments:
        st.write(appointment)
    
    if st.button("Make an appointment!"):
        st.session_state.new_appointment_button = True
    
    if st.session_state.new_appointment_button:
        appointment_form(current_patient)

def get_patient_appointment_details(patient_id, patients_file, appointments_file, patient_appointments_file, doctors_file):
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
        return f"No appointments found for patient ID {patient_id}."
    
    # Extract relevant columns and patient details
    patient_name = patient_info.iloc[0]['Name']
    details = []
    for _, row in patient_appointments.iterrows():
        detail = {
            "Patient Name": patient_name,
            "Appointment ID": row["Appointment ID"],
            "Status": row["Status"].title(),
            "Date": row["Date"],
            "Diagnosis": row["Diagnostic"] if row["Diagnostic"] != "[TBA]" else "Not Available",
            "Symptoms": row["Symptoms"] if row["Symptoms"] != "[TBA]" else "Not Available",
            "Treatment": row["Treatment"] if row["Treatment"] != "[TBA]" else "Not Available",
            "Doctor Name": row["Name"],
        }
        details.append(detail)

    return details

def login(df):
    st.title("Welcome back to :blue[Health First]")
    patient_id = st.text_input("Login with ID", value="")
    
    # check if ID exists
    patient_exists = not df[(df['Patient ID'].str.upper() == patient_id.upper())].empty

    if patient_exists:
        run_patient_dashboard(patient_id)
    else:
        if patient_id != "":
            st.error(f"No patient with ID: {patient_id.upper()} exists!")
      
def appointment_form(current_patient: Patient):
    st.divider()
    st.title('Appointment Request Form')
    st.write('Please proceed with your appointment request.')

    appointment_date = st.date_input('Please choose the available date', format="MM/DD/YYYY").strftime("%m/%d/%Y")
    complaint = st.text_input('Describe how you feel')

    if st.button('Save Appointment'):
        if not complaint:
            st.error("Please fill in your complaint!")
        else:
            appointment_request = Appointment(appointment_date, 0, complaint)
            current_patient.add_appointment(appointment_request)
            st.success('Your appointment has been saved!')
            # reset appointment form button
            st.session_state.new_appointment_button = False
            return appointment_request

# ------------------------------------

st.set_page_config(page_title="Health First Patient", layout="centered")
st.title("Patient Dashboard")

df = pd.read_csv("./dataset/patients.csv", sep=';')

if "button_pressed" not in st.session_state:
    st.session_state.button_pressed = None

if "new_appointment_button" not in st.session_state:
        st.session_state.new_appointment_button = False

col1, col2 = st.columns([1,5])
with col1:
    if st.button("I'm a patient"):
        st.session_state.button_pressed = "patient"
with col2:
    if st.button("I'm new"):
        st.session_state.button_pressed = "new"

        # reset new appointment button when switched to signup page
        st.session_state.new_appointment_button = False

st.divider()

if st.session_state.button_pressed == "patient":
    login(df)

elif st.session_state.button_pressed == "new":
    sign_up()

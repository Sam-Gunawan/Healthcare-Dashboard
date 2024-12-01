import streamlit as st
import pandas as pd
from healthcare_classes import *
import time


def complete_appointment_form(current_doctor: Doctor, doctor_appointments): 
    st.title('Post-Appointment Form')

    appointment_id = st.text_input('Appointment ID').upper()
    status = st.selectbox('Pending/Completed', ['Pending', 'Completed'])
    diagnostic = st.text_input('Diagnostic', disabled=(status == 'Pending')) 
    symptoms = st.text_input('Symptoms', disabled=(status == 'Pending'))
    treatment =  st.text_input('Treatment', disabled=(status == 'Pending'))

    valid_appointment_ids = [record["Appointment ID"] for record in doctor_appointments]

    col1, col2 = st.columns([1, 6])
    if col1.button('Complete'):
        if appointment_id not in valid_appointment_ids:
            st.warning("Invalid appointment ID. Either it doesn't exist, or it's not your assigned appointment.")
        elif status == "Pending":
            st.warning("Cannot save summary while the status is Pending!")
        else:
            patient_df = pd.read_csv(PATIENTS_FILE, sep=';')
            assigned_appointments_df = pd.read_csv(APPOINTMENT_ASSIGNMENT_FILE, sep=';')
            current_patient_id = assigned_appointments_df.loc[assigned_appointments_df['appointment_id'] == appointment_id, "patient_id"].astype(str).values[0]
            patient_data = patient_df[(patient_df['Patient ID'].str.upper() == current_patient_id.upper())].values
            
            patient_id = patient_data[0][0]
            patient_name = patient_data[0][1]
            patient_gender = patient_data[0][2]
            patient_dob = patient_data[0][3]
            patient_number = patient_data[0][4]
            patient_email = patient_data[0][5]

            current_patient = Patient(patient_name, patient_email, patient_gender, patient_dob, patient_number, [""], patient_id)
            new_medical_record = current_doctor.complete_appointment(APPOINTMENTS_FILE, appointment_id, diagnostic, symptoms, treatment)

            # automatically adds to patient's medical history
            current_patient.add_medical_history(new_medical_record)

            # reset complete appointment form button
            st.session_state.complete_appointment_button = False
            
            # play loading bar for ux purposes before refreshing the page and updating appointments
            progress_text = "Creating your appointment. Please wait."
            saving_appointment_bar = st.progress(0, text=progress_text)
            for perent_complete in range(100):
                time.sleep(0.02)
                saving_appointment_bar.progress(perent_complete + 1, text=progress_text)
            time.sleep(0.5)
            st.success('Successfully Completed!')
            time.sleep(1.5)
            st.rerun()
        
    if col2.button('Cancel'):
        st.session_state.complete_appointment_button = False
        st.rerun()

def get_doctor_appointment_details(doctor_id, patients_file, appointments_file, doctor_appointments_file, doctors_file):
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

def run_doctor_dashboard(doctor_id, df):
    # search for doctor data in dataframe
    doctor_data = df[(df['Doctor ID'].str.upper() == doctor_id.upper())].values
    
    doctor_id = doctor_data[0][0]
    doctor_name = doctor_data[0][1]
    doctor_specialization = doctor_data[0][2]
    doctor_office = doctor_data[0][3]

    current_doctor = Doctor(doctor_name, doctor_id, doctor_specialization, doctor_office)

    st.subheader("Profile")
    st.write("Doctor ID: ", doctor_id)
    st.write("Name: ", doctor_name)
    st.write("Specialization: ", doctor_specialization)
    st.write("Office: ", doctor_office)

    st.divider()
    doctor_appointments = get_doctor_appointment_details(doctor_id, PATIENTS_FILE, APPOINTMENTS_FILE, APPOINTMENT_ASSIGNMENT_FILE, DOCTORS_FILE)

    if doctor_appointments == "empty":
        st.write("No appointments yet...")
    else:
        doctor_appointments_df = pd.DataFrame(doctor_appointments)

        st.subheader(":blue[Pending] appointments")
        df_pending = doctor_appointments_df[doctor_appointments_df['Status'] == "Pending"]
        df_pending = df_pending.drop(columns=['Status', 'Symptoms', 'Diagnosis', 'Treatment'])
        if df_pending.empty:
            st.markdown("No appointments found")
        else:
            st.write(df_pending)
            if st.button("Complete appointment"):
                st.session_state.complete_appointment_button = True
            if st.session_state.complete_appointment_button:
                complete_appointment_form(current_doctor, doctor_appointments)

        st.divider()

        st.subheader(":green[Completed] appointments")
        df_completed = doctor_appointments_df[doctor_appointments_df['Status'] == "Completed"]
        df_completed = df_completed.drop(columns=['Status'])
        if df_completed.empty:
            st.markdown("No appointments found")
        else:
            st.write(df_completed)
        

def login(df):
    st.title("Let's get to work!")
    doctor_id = st.text_input("Login with ID", value="")
    
    # check if ID exists
    doctor_exists = not df[(df['Doctor ID'].str.upper() == doctor_id.upper())].empty

    if doctor_exists:
        run_doctor_dashboard(doctor_id, df)
    else:
        if doctor_id != "":
            st.error(f"No doctor with ID: {doctor_id.upper()} exists!")
      

st.set_page_config("Health First Doctors", layout="centered")
st.title("Doctor Dashboard")

if "complete_appointment_button" not in st.session_state:
    st.session_state.complete_appointment_button = False

df = pd.read_csv(DOCTORS_FILE, sep=';')

st.divider()

login(df)
import streamlit as st

def app():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "input_patient_profile"

    if st.session_state.current_page == "input_patient_profile":
        patient_profile()
    elif st.session_state.current_page == "request_appointment":
        appointment_form()

def patient_profile():
    st.title('Welcome to :blue[Health First]')

    patient_name = st.text_input('Name')
    patient_gender = st.selectbox('Gender', ['Male', 'Female'])
    patient_dob = st.date_input('Date of Birth')
    patient_number = st.text_input('Contact Number') 
    patient_email = st.text_input('Email Address')

    if st.button('Save'):
        if not patient_name:
            st.error("Name is required!")
        elif not patient_gender:
            st.error("Gender is required!")
        elif not patient_number:
            st.error("Contact Number is required!")
        elif not patient_email:
            st.error("Email Address is required!")
        else:
            st.session_state.current_page = "request_appointment"

def appointment_form():
    st.title('Appointment Request Form')
    st.write('Thank you for telling :blue[Health First] who you are, please proceed with your appointment request.')

    appoint_date = st.date_input('Please choose the available date')
    complaints = st.text_input('Please tell us what you are feeling')

    if st.button('Save Appointment'):
        if not complaints:
            st.error("Please describe your complaints!")
        else:
            st.success('Your appointment has been saved!')

    if st.button('Back'):
        st.session_state.current_page = "input_patient_profile"

app()
